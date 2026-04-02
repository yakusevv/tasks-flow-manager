import pytest

from core.task_registry import TaskNotFoundError, TaskRegistry
from models.flow import FlowContextSchema
from tasks.base_task import BaseTask


class DummyTask(BaseTask):
    name = "dummy"

    async def run(self, context: FlowContextSchema) -> dict:
        return {}


def test_task_registry_register_and_get():
    registry = TaskRegistry()
    task = DummyTask()

    registry.register(task)

    assert registry.get("dummy") is task


def test_task_registry_get_not_registered_raises():
    registry = TaskRegistry()

    with pytest.raises(TaskNotFoundError) as exc_info:
        registry.get("missing")

    assert "missing" in str(exc_info.value)


def test_task_registry_all_returns_list():
    registry = TaskRegistry()
    t1, t2 = DummyTask(), DummyTask()
    t2.name = "dummy2"

    registry.register(t1)
    registry.register(t2)
    tasks = registry.all()

    assert len(tasks) == 2
    assert t1 in tasks
    assert t2 in tasks
