import pytest
from starlette.testclient import TestClient

from core.task_registry import TaskRegistry
from helpers import make_flow_config, make_mock_task
from models.flow import FlowConfigSchema, TaskOutcomeEnum


@pytest.fixture
def flow_config() -> FlowConfigSchema:
    return make_flow_config()


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
