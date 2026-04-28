from unittest.mock import AsyncMock

from core.flows.exceptions import FlowAlreadyExistsError
from helpers import make_flow_config


def test_create_flow_success(client, mock_flow_loader: AsyncMock):
    # given
    flow = make_flow_config("new_flow")
    mock_flow_loader.create = AsyncMock(return_value=flow)

    # when
    response = client.post("/v1/flows", json=flow.model_dump())

    # then
    assert response.status_code == 201
    assert response.json()["id"] == "new_flow"


def test_create_flow_conflict(client, mock_flow_loader: AsyncMock):
    # given
    flow = make_flow_config("existing_flow")
    mock_flow_loader.create = AsyncMock(side_effect=FlowAlreadyExistsError("existing_flow"))

    # when
    response = client.post("/v1/flows", json=flow.model_dump())

    # then
    assert response.status_code == 409
    assert "existing_flow" in response.json()["detail"]
