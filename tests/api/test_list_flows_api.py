from unittest.mock import patch

from helpers import make_flow_config


def test_list_flows(client):
    flows = [make_flow_config("flow1"), make_flow_config("flow2")]
    with patch("api.api_v1.flow.flow_loader.list_all", return_value=flows):
        response = client.get("/v1/flows")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == "flow1"
    assert data[1]["id"] == "flow2"


def test_list_flows_empty(client):
    with patch("api.api_v1.flow.flow_loader.list_all", return_value=[]):
        response = client.get("/v1/flows")

    assert response.status_code == 200
    assert response.json() == []
