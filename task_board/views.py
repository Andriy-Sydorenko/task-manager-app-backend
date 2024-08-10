from drf_spectacular.utils import extend_schema_view
from rest_framework import permissions, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from task_board import documentation
from task_board.models import Task, TaskBoard
from task_board.serializers import TaskBoardSerializer, TaskSerializer


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
        return self.queryset.filter(created_by=self.request.user)


# TODO: implement pagination
@extend_schema_view(**documentation.TASK_BOARD_DOCS)
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        JWTAuthentication,
    ]

    lookup_field = "task_uuid"

    def get_queryset(self):
        return self.queryset.filter(task_board__created_by=self.request.user)
