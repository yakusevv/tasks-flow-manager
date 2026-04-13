from unittest.mock import AsyncMock

from helpers import make_flow_config


def test_list_flows(client):
    # given
    from core.dependencies import get_flow_loader
    from main import app

    flows = [make_flow_config("flow1"), make_flow_config("flow2")]
    mock_loader = AsyncMock()
    mock_loader.list_all = AsyncMock(return_value=flows)
    app.dependency_overrides[get_flow_loader] = lambda: mock_loader

    # when
    response = client.get("/v1/flows")

    # then
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == "flow1"
    assert data[1]["id"] == "flow2"


def test_list_flows_empty(client):
    # given
    from core.dependencies import get_flow_loader
    from main import app

    mock_loader = AsyncMock()
    mock_loader.list_all = AsyncMock(return_value=[])
    app.dependency_overrides[get_flow_loader] = lambda: mock_loader

    # when
    response = client.get("/v1/flows")

    # then
    assert response.status_code == 200
    assert response.json() == []
