from rest_framework import exceptions, serializers

from task_board.models import Task, TaskBoard


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            "task_uuid",
            "name",
            "description",
            "status",
            "created_at",
            "updated_at",
            "postponed_to",
        )


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "status",
            "postponed_to",
        ]


class TaskCreateSerializer(serializers.ModelSerializer):
    task_board_uuid = serializers.UUIDField(write_only=True)

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "task_board_uuid",
            "created_at",
            "updated_at",
            "postponed_to",
            "status",
            "task_uuid",
        ]
        read_only_fields = ["created_at", "updated_at", "postponed_to", "status", "task_uuid"]

    def validate(self, data):
        if "task_board_uuid" not in data:
            raise exceptions.ValidationError({"task_board_uuid": "Task board UUID is required."})
        return data

    def create(self, validated_data):
        task_board_uuid = validated_data.pop("task_board_uuid")
        try:
            task_board = TaskBoard.objects.get(board_uuid=task_board_uuid)
        except TaskBoard.DoesNotExist:
            raise exceptions.ValidationError({"task_board_uuid": "Invalid Task board UUID."})
        validated_data["task_board"] = task_board
        return Task.objects.create(**validated_data)


class TaskBoardSerializer(serializers.ModelSerializer):
    task_count = serializers.IntegerField(read_only=True)
    in_progress_task_count = serializers.IntegerField(read_only=True)
    done_task_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = TaskBoard
        fields = (
            "board_uuid",
            "name",
            "description",
            "task_count",
            "in_progress_task_count",
            "done_task_count",
            "created_at",
            "updated_at",
        )


class TaskBoarDetailSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True, source="task_set")
    task_count = serializers.IntegerField(read_only=True)
    in_progress_task_count = serializers.IntegerField(read_only=True)
    done_task_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = TaskBoard
        fields = (
            "tasks",
            "board_uuid",
            "name",
            "description",
            "task_count",
            "in_progress_task_count",
            "done_task_count",
            "created_at",
            "updated_at",
        )


class TaskBoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskBoard
        fields = (
            "name",
            "description",
            "created_at",
            "updated_at",
            "board_uuid",
        )

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
