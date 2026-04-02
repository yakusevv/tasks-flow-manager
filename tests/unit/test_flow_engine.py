import pytest

from helpers import make_flow_config, make_mock_task
from core.flow_engine import FlowCycleError, FlowEngine
from core.task_registry import TaskNotFoundError, TaskRegistry
from models.flow import FlowOutcomeEnum, TaskOutcomeEnum


@pytest.fixture
def flow_config():
    return make_flow_config()


@pytest.fixture
def registry_all_success() -> TaskRegistry:
    registry = TaskRegistry()

    registry.register(make_mock_task("task1", TaskOutcomeEnum.SUCCESS, {"r": 1}))
    registry.register(make_mock_task("task2", TaskOutcomeEnum.SUCCESS, {"r": 2}))
    registry.register(make_mock_task("task3", TaskOutcomeEnum.SUCCESS, {"r": 3}))

    return registry


async def test_flow_engine_run_all_tasks_succeed(flow_config, registry_all_success):
    engine = FlowEngine(config=flow_config, registry=registry_all_success)

    result = await engine.run()

    assert result.final_outcome == FlowOutcomeEnum.COMPLETED
    assert result.completed_tasks == ["task1", "task2", "task3"]
    assert result.errors == []


async def test_flow_engine_run_task_fails_ends_early(flow_config):
    registry = TaskRegistry()
    registry.register(make_mock_task("task1", TaskOutcomeEnum.SUCCESS))
    registry.register(make_mock_task("task2", TaskOutcomeEnum.FAILURE, error="boom"))
    registry.register(make_mock_task("task3", TaskOutcomeEnum.SUCCESS))

    engine = FlowEngine(config=flow_config, registry=registry)
    result = await engine.run()

    assert result.final_outcome == FlowOutcomeEnum.ENDED_EARLY
    assert "task2" in result.completed_tasks
    assert "task3" not in result.completed_tasks
    assert any("task2" in e for e in result.errors)


async def test_flow_engine_run_cycle_raises():
    config = make_flow_config(
        tasks=[
            {"name": "task1", "description": "T1"},
            {"name": "task2", "description": "T2"},
        ],
        conditions=[
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
                "target_task_success": "task1",  # loop back
                "target_task_failure": "end",
            },
        ],
    )
    registry = TaskRegistry()
    registry.register(make_mock_task("task1", TaskOutcomeEnum.SUCCESS))
    registry.register(make_mock_task("task2", TaskOutcomeEnum.SUCCESS))

    engine = FlowEngine(config=config, registry=registry)
    with pytest.raises(FlowCycleError):
        await engine.run()


async def test_flow_engine_run_task_not_in_registry_raises(flow_config):
    empty_registry = TaskRegistry()
    engine = FlowEngine(config=flow_config, registry=empty_registry)
    with pytest.raises(TaskNotFoundError):
        await engine.run()
