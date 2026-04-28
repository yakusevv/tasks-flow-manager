from unittest.mock import AsyncMock

from core.flows.exceptions import FlowNotFoundError


def test_delete_flow_success(client, mock_flow_loader: AsyncMock):
    # given
    mock_flow_loader.delete = AsyncMock(return_value=None)

    # when
    response = client.delete("/v1/flows/flow1")

    # then
    assert response.status_code == 204
    mock_flow_loader.delete.assert_called_once_with("flow1")


def test_delete_flow_not_found(client, mock_flow_loader: AsyncMock):
    # given
    mock_flow_loader.delete = AsyncMock(side_effect=FlowNotFoundError("missing"))

    # when
    response = client.delete("/v1/flows/missing")

    # then
    assert response.status_code == 404
    assert "missing" in response.json()["detail"]
