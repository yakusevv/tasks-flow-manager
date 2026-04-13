from unittest.mock import AsyncMock

import pytest
from starlette.testclient import TestClient

from core.dependencies import get_flow_loader
from core.task_registry import TaskRegistry
from helpers import make_flow_config, make_mock_task
from main import app
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
    return TestClient(app)


@pytest.fixture
def mock_flow_loader() -> AsyncMock:
    loader = AsyncMock()
    app.dependency_overrides[get_flow_loader] = lambda: loader
    return loader


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    yield
    app.dependency_overrides.pop(get_flow_loader, None)
