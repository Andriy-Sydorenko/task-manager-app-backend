from django.urls import include, path
from rest_framework.routers import DefaultRouter

from task_board.views import TaskBoardViewSet, TaskViewSet

router = DefaultRouter()
router.register(r"task-boards", TaskBoardViewSet, basename="taskboard")
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("", include(router.urls)),
]
