from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from task_board.models import DailyTaskStats, Task


@receiver(pre_save, sender=Task)
def track_previous_status_signal(sender, instance, **kwargs):
    if instance.pk:
        instance._previous_status = Task.objects.get(pk=instance.pk).status
    else:
        instance._previous_status = None


@receiver(post_save, sender=Task)
def update_daily_task_stats_signal(sender, instance, **kwargs):

    today = timezone.localtime().date()
    print(today)
    stats, created = DailyTaskStats.objects.get_or_create(date=today, user=instance.task_board.created_by)
    previous_status = getattr(instance, "_previous_status", None)

    if previous_status == "TODO":
        stats.todo_count -= 1
    elif previous_status == "IN_PROGRESS":
        stats.in_progress_count -= 1
    elif previous_status == "DONE":
        stats.done_count -= 1

    if instance.status == "TODO":
        stats.todo_count += 1
    elif instance.status == "IN_PROGRESS":
        stats.in_progress_count += 1
    elif instance.status == "DONE":
        stats.done_count += 1

    stats.save()
