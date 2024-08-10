from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from task_board.views import TaskBoardViewSet, TaskViewSet

router = DefaultRouter()
router.register(r"task-boards", TaskBoardViewSet)
router.register(r"tasks", TaskViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
]
