from unittest.mock import AsyncMock

from helpers import make_flow_config


def test_list_flows(client, mock_flow_loader: AsyncMock):
    # given
    flows = [make_flow_config("flow1"), make_flow_config("flow2")]
    mock_flow_loader.list_all = AsyncMock(return_value=flows)

    # when
    response = client.get("/v1/flows")

    # then
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == "flow1"
    assert data[1]["id"] == "flow2"


def test_list_flows_empty(client, mock_flow_loader: AsyncMock):
    # given
    mock_flow_loader.list_all = AsyncMock(return_value=[])

    # when
    response = client.get("/v1/flows")

    # then
    assert response.status_code == 200
    assert response.json() == []
