import uuid

from django.conf import settings
from django.db import models

from task_board.choices import TaskStatus


class TaskBoard(models.Model):
    board_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def task_count(self):
        return self.task_set.count()

    def in_progress_task_count(self):
        return self.task_set.filter(status=TaskStatus.IN_PROGRESS).count()

    def done_task_count(self):
        return self.task_set.filter(status=TaskStatus.DONE).count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]


class Task(models.Model):
    task_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    task_board = models.ForeignKey(TaskBoard, to_field="board_uuid", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # TODO: add task postpone functionality
    postponed_to = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class DailyTaskStats(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    todo_count = models.PositiveIntegerField(default=0)
    in_progress_count = models.PositiveIntegerField(default=0)
    done_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("date",)
