def backfill_daily_task_stats(task) -> None:
    from task_board.models import DailyTaskStats, Task

    date = task.updated_at.date()
    stats, created = DailyTaskStats.objects.get_or_create(date=date, user=task.task_board.created_by)
    stats.todo_count = Task.objects.filter(status="TODO", updated_at__date=date).count()
    stats.in_progress_count = Task.objects.filter(status="IN_PROGRESS", updated_at__date=date).count()
    stats.done_count = Task.objects.filter(status="DONE", updated_at__date=date).count()
    stats.save()
