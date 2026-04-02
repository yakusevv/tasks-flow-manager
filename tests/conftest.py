import pytest
from starlette.testclient import TestClient

from core.task_registry import TaskRegistry
from models.flow import (
    ConditionConfigSchema,
    FlowConfigSchema,
    FlowContextSchema,
    TaskConfigSchema,
    TaskOutcomeEnum,
    TaskResultSchema,
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


@pytest.fixture
def flow_config() -> FlowConfigSchema:
    return make_flow_config()


def make_mock_task(task_name: str, outcome: TaskOutcomeEnum, data: dict | None = None, error: str | None = None) -> BaseTask:
    class MockTask(BaseTask):
        name = task_name

        async def run(self, context: FlowContextSchema) -> dict | None:
            if outcome == TaskOutcomeEnum.FAILURE:
                raise RuntimeError(error or f"{task_name} failed")
            return data

    return MockTask()


@pytest.fixture
def registry_with_mocks() -> TaskRegistry:
    registry = TaskRegistry()
    registry.register(make_mock_task("task1", TaskOutcomeEnum.SUCCESS, {"result": "t1"}))
    registry.register(make_mock_task("task2", TaskOutcomeEnum.SUCCESS, {"result": "t2"}))
    registry.register(make_mock_task("task3", TaskOutcomeEnum.SUCCESS, {"result": "t3"}))
    return registry


@pytest.fixture
def client():
    from main import app
    return TestClient(app)
