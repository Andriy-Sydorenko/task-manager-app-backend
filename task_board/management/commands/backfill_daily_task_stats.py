from django.core.management.base import BaseCommand

from task_board.models import Task
from task_board.utils import backfill_daily_task_stats


class Command(BaseCommand):
    help = "Backfill DailyTaskStats for existing tasks"

    def handle(self, *args, **kwargs):
        tasks = Task.objects.all()
        for task in tasks:
            backfill_daily_task_stats(task)
        self.stdout.write(self.style.SUCCESS("Successfully backfilled DailyTaskStats"))
