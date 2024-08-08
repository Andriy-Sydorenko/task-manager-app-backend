from django.contrib import admin

from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "nickname",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    search_fields = (
        "email",
        "nickname",
    )
