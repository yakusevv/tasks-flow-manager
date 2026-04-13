from unittest.mock import AsyncMock, MagicMock, patch

from core.flow_engine import FlowCycleError
from core.flow_loader import FlowNotFoundError
from models.flow import FlowOutcomeEnum, FlowRunResultSchema


def test_run_flow_success(client, mock_flow_loader: AsyncMock):
    # given
    mock_flow_loader.load = AsyncMock(return_value=MagicMock())

    mock_result = FlowRunResultSchema(
        flow_id="flow123",
        completed_tasks=["task1", "task2", "task3"],
        final_outcome=FlowOutcomeEnum.COMPLETED,
        errors=[],
    )
    mock_engine = MagicMock()
    mock_engine.run = AsyncMock(return_value=mock_result)

    # when
    with patch("api.api_v1.flow.FlowEngine", return_value=mock_engine):
        response = client.post("/v1/flows/flow123/run")

    # then
    assert response.status_code == 200
    data = response.json()
    assert data["flow_id"] == "flow123"
    assert data["final_outcome"] == FlowOutcomeEnum.COMPLETED
    assert data["completed_tasks"] == ["task1", "task2", "task3"]


def test_run_flow_not_found(client, mock_flow_loader: AsyncMock):
    # given
    mock_flow_loader.load = AsyncMock(side_effect=FlowNotFoundError("missing"))

    # when
    response = client.post("/v1/flows/missing/run")

    # then
    assert response.status_code == 404
    assert "missing" in response.json()["detail"]


def test_run_flow_cycle_error(client, mock_flow_loader: AsyncMock):
    # given
    mock_flow_loader.load = AsyncMock(return_value=MagicMock())

    mock_engine = MagicMock()
    mock_engine.run = AsyncMock(side_effect=FlowCycleError("task1"))

    # when
    with patch("api.api_v1.flow.FlowEngine", return_value=mock_engine):
        response = client.post("/v1/flows/flow123/run")

    # then
    assert response.status_code == 409
    assert "task1" in response.json()["detail"]
