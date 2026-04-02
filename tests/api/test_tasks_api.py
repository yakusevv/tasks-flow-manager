from unittest.mock import patch

from models.flow import TaskInfoSchema


def test_list_tasks(client):
    mock_tasks = [TaskInfoSchema(name="task1"), TaskInfoSchema(name="task2")]
    with patch("api.api_v1.tasks.task_registry.all", return_value=mock_tasks):
        response = client.get("/v1/tasks")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "task1"
    assert data[1]["name"] == "task2"


def test_list_tasks_empty(client):
    with patch("api.api_v1.tasks.task_registry.all", return_value=[]):
        response = client.get("/v1/tasks")

    assert response.status_code == 200
    assert response.json() == []
