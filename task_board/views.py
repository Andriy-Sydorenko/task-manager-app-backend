from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema_view
from rest_framework import permissions, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from task_board import documentation
from task_board.models import Task, TaskBoard
from task_board.serializers import (
    TaskBoardCreateSerializer,
    TaskBoarDetailSerializer,
    TaskBoardSerializer,
    TaskCreateSerializer,
    TaskSerializer,
    TaskUpdateSerializer,
)


# TODO: implement pagination
# TODO: implement ordering
# TODO: implement filtering
# TODO: implement search
@extend_schema_view(**documentation.TASK_BOARD_DOCS)
class TaskBoardViewSet(viewsets.ModelViewSet):
    queryset = TaskBoard.objects.all()
    serializer_class = TaskBoardSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        JWTAuthentication,
    ]

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


# TODO: implement pagination
@extend_schema_view(**documentation.TASK_DOCS)
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        JWTAuthentication,
    ]

    lookup_field = "task_uuid"

    def get_queryset(self):
        return self.queryset.filter(task_board__created_by=self.request.user).select_related("task_board")

    def get_serializer_class(self):
        if self.action == "partial_update":
            return TaskUpdateSerializer
        if self.action == "create":
            return TaskCreateSerializer
        return super().get_serializer_class()
