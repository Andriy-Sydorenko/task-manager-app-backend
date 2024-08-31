from datetime import timedelta

from django.db.models import Prefetch
from django.utils import timezone
from drf_spectacular.utils import extend_schema_view
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from task_board import documentation
from task_board.mixins import FilterMixin
from task_board.models import DailyTaskStats, Task, TaskBoard
from task_board.pagination import Pagination
from task_board.serializers import (
    TaskBoardCreateSerializer,
    TaskBoarDetailSerializer,
    TaskBoardSerializer,
    TaskCreateSerializer,
    TaskSerializer,
    TaskUpdateSerializer,
)


@extend_schema_view(**documentation.TASK_BOARD_DOCS)
class TaskBoardViewSet(viewsets.ModelViewSet, FilterMixin):
    queryset = TaskBoard.objects.all()
    serializer_class = TaskBoardSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        JWTAuthentication,
    ]
    pagination_class = Pagination

    lookup_field = "board_uuid"

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        queryset = self.queryset.prefetch_related(Prefetch("task_set", queryset=Task.objects.all()))
        return queryset.filter(created_by=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return TaskBoardCreateSerializer
        if self.action == "retrieve" or self.action == "partial_update":
            return TaskBoarDetailSerializer
        return super().get_serializer_class()


@extend_schema_view(**documentation.TASK_DOCS)
class TaskViewSet(viewsets.ModelViewSet, FilterMixin):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        JWTAuthentication,
    ]
    pagination_class = Pagination

    lookup_field = "task_uuid"

    def get_queryset(self):
        return self.queryset.filter(task_board__created_by=self.request.user).select_related("task_board")

    def get_serializer_class(self):
        if self.action == "partial_update":
            return TaskUpdateSerializer
        if self.action == "create":
            return TaskCreateSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=["get"], url_path="dashboard")
    def dashboard(self, request):
        query_params = request.query_params
        start_date = query_params.get("start_date")
        end_date = query_params.get("end_date")
        if not start_date and not end_date:
            end_date = timezone.localtime().date()
            start_date = end_date - timedelta(days=7)

        stats = DailyTaskStats.objects.filter(user=request.user, date__range=[start_date, end_date]).values(
            "date", "todo_count", "in_progress_count", "done_count"
        )

        response_data = {
            stat["date"].isoformat(): {
                "TODO": stat["todo_count"],
                "IN_PROGRESS": stat["in_progress_count"],
                "DONE": stat["done_count"],
            }
            for stat in stats
        }

        return Response(response_data)
