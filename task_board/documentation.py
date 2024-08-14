from drf_spectacular.utils import OpenApiExample, extend_schema

TASK_BOARD_DOCS = {
    "list": extend_schema(
        summary="List all task boards",
        description="Retrieve a list of all task boards created by the authenticated user.",
        examples=[
            OpenApiExample(
                "Example for list",
                value={
                    "board_uuid": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Project Alpha",
                    "description": "Tasks for Project Alpha",
                },
            )
        ],
    ),
    "retrieve": extend_schema(
        summary="Retrieve a task board",
        description="Retrieve a specific task board by its UUID.",
        examples=[
            OpenApiExample(
                "Example for retrieve",
                value={
                    "board_uuid": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Project Alpha",
                    "description": "Tasks for Project Alpha",
                },
            )
        ],
    ),
    "create": extend_schema(
        summary="Create a new task board",
        description="Create a new task board with the provided data.",
        examples=[
            OpenApiExample(
                "Example for create", value={"name": "Project Beta", "description": "Tasks for Project Beta"}
            )
        ],
    ),
    "update": extend_schema(
        summary="Update a task board",
        description="Update an existing task board with the provided data.",
        examples=[
            OpenApiExample(
                "Example for update", value={"name": "Project Gamma", "description": "Updated tasks for Project Gamma"}
            )
        ],
    ),
    "partial_update": extend_schema(
        summary="Partially update a task board",
        description="Partially update an existing task board with the provided data.",
        examples=[
            OpenApiExample(
                "Example for partial update", value={"description": "Partially updated tasks for Project Delta"}
            )
        ],
    ),
    "destroy": extend_schema(
        summary="Delete a task board",
        description="Delete a specific task board by its UUID.",
    ),
}

TASK_DOCS = {
    "list": extend_schema(
        summary="List all tasks",
        description="Retrieve a list of all tasks created by the authenticated user.",
        examples=[
            OpenApiExample(
                "Example 1",
                value={
                    "task_uuid": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Task 1",
                    "description": "Description for Task 1",
                    "task_board": "123e4567-e89b-12d3-a456-426614174000",
                    "status": "TODO",
                    "created_at": "2023-10-01T12:00:00Z",
                    "updated_at": "2023-10-01T12:00:00Z",
                    "postponed_to": None,
                },
            )
        ],
    ),
    "retrieve": extend_schema(
        summary="Retrieve a task",
        description="Retrieve a specific task by its UUID.",
        examples=[
            OpenApiExample(
                "Example for list",
                value={
                    "task_uuid": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Task 1",
                    "description": "Description for Task 1",
                    "task_board": "123e4567-e89b-12d3-a456-426614174000",
                    "status": "TODO",
                    "created_at": "2023-10-01T12:00:00Z",
                    "updated_at": "2023-10-01T12:00:00Z",
                    "postponed_to": None,
                },
            )
        ],
    ),
    "create": extend_schema(
        summary="Create a new task",
        description="Create a new task with the provided data.",
        examples=[
            OpenApiExample(
                "Example for create",
                value={
                    "name": "Task 2",
                    "description": "Description for Task 2",
                    "task_board_uuid": "123e4567-e89b-12d3-a456-426614174000",
                    "status": "TODO",
                },
            )
        ],
    ),
    "update": extend_schema(
        summary="Update a task",
        description="Update an existing task with the provided data.",
        examples=[
            OpenApiExample(
                "Example for update",
                value={"name": "Task 3", "description": "Updated description for Task 3", "status": "IN_PROGRESS"},
            )
        ],
    ),
    "partial_update": extend_schema(
        summary="Partially update a task",
        description="Partially update an existing task with the provided data.",
        examples=[
            OpenApiExample(
                "Example for partial update", value={"description": "Partially updated description for Task 4"}
            )
        ],
    ),
    "destroy": extend_schema(
        summary="Delete a task",
        description="Delete a specific task by its UUID.",
    ),
}
