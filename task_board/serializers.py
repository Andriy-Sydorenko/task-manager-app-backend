from rest_framework import serializers

from task_board.models import Task, TaskBoard


class TaskBoardSerializer(serializers.ModelSerializer):
    task_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = TaskBoard
        exclude = ("created_by",)

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class TaskSerializer(serializers.ModelSerializer):
    task_board_uuid = serializers.UUIDField(write_only=True)

    class Meta:
        model = Task
        fields = (
            "task_uuid",
            "name",
            "description",
            "task_board_uuid",
            "status",
            "created_at",
            "updated_at",
            "postponed_to",
        )

    def create(self, validated_data):
        task_board_uuid = validated_data.pop("task_board_uuid")
        task_board = TaskBoard.objects.get(board_uuid=task_board_uuid)
        task = Task.objects.create(task_board=task_board, **validated_data)
        return task
