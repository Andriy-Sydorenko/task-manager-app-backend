from django.contrib import admin

from task_board.models import Task, TaskBoard


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "task_uuid",
        "name",
        "description",
        "task_board",
        "status",
        "created_at",
        "updated_at",
        "postponed_to",
    )
    search_fields = ("name", "description", "task_board__name", "status")
    list_filter = ("status", "created_at", "updated_at")


@admin.register(TaskBoard)
class TaskBoardAdmin(admin.ModelAdmin):
    list_display = (
        "board_uuid",
        "name",
        "description",
        "created_at",
        "updated_at",
        "task_count",
    )
    search_fields = ("name", "description")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_by", "task_count")

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
