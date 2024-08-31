import requests
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig
from django.conf import settings


class TaskBoardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "task_board"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._scheduler = BackgroundScheduler(executors={"default": ThreadPoolExecutor(1)})

    def ready(self):
        import task_board.signals  # noqa

        if not hasattr(self, "scheduler"):
            self._scheduler.start()
            self.add_scheduled_jobs()

    def add_scheduled_jobs(self):
        @self._scheduler.scheduled_job("interval", seconds=settings.PING_PONG_INTERVAL)
        def send_get_request():
            url = f"{settings.RENDER_BACKEND_URL}/api/tasks/"
            try:
                requests.get(url)
                print(f"Successful GET request to {url}")
            except requests.exceptions.RequestException as e:
                print(f"Error during GET request to {url}: {str(e)}")
