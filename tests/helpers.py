from models.flow import (
    FlowConfigSchema,
    FlowContextSchema,
    TaskOutcomeEnum,
)
from tasks.base_task import BaseTask


def make_flow_config(
    flow_id: str = "test_flow",
    tasks: list[dict] | None = None,
    conditions: list[dict] | None = None,
    start_task: str = "task1",
) -> FlowConfigSchema:
    tasks = tasks or [
        {"name": "task1", "description": "Task 1"},
        {"name": "task2", "description": "Task 2"},
        {"name": "task3", "description": "Task 3"},
    ]
    conditions = conditions or [
        {
            "name": "cond1",
            "description": "",
            "source_task": "task1",
            "outcome": "success",
            "target_task_success": "task2",
            "target_task_failure": "end",
        },
        {
            "name": "cond2",
            "description": "",
            "source_task": "task2",
            "outcome": "success",
            "target_task_success": "task3",
            "target_task_failure": "end",
        },
    ]
    return FlowConfigSchema.model_validate(
        {
            "id": flow_id,
            "name": "Test Flow",
            "start_task": start_task,
            "tasks": tasks,
            "conditions": conditions,
        }
    )


def make_mock_task(
    task_name: str,
    outcome: TaskOutcomeEnum,
    data: dict | None = None,
    error: str | None = None,
) -> BaseTask:
    class MockTask(BaseTask):
        name = task_name

        async def run(self, context: FlowContextSchema) -> dict | None:
            if outcome == TaskOutcomeEnum.FAILURE:
                raise RuntimeError(error or f"{task_name} failed")
            return data

    return MockTask()
