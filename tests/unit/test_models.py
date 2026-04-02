import pytest

from models.flow import FlowConfigSchema


BASE = {
    "id": "f1",
    "name": "Test Flow",
    "start_task": "task1",
    "tasks": [
        {"name": "task1", "description": "T1"},
        {"name": "task2", "description": "T2"},
    ],
    "conditions": [
        {
            "name": "cond1",
            "description": "",
            "source_task": "task1",
            "outcome": "success",
            "target_task_success": "task2",
            "target_task_failure": "end",
        }
    ],
}


def test_valid_config_passes():
    config = FlowConfigSchema.model_validate(BASE)

    assert config.id == "f1"
    assert len(config.tasks) == 2


def test_invalid_start_task():
    data = {**BASE, "start_task": "nonexistent"}

    with pytest.raises(ValueError):
        FlowConfigSchema.model_validate(data)


def test_duplicate_task_name():
    data = {
        **BASE,
        "tasks": [
            {"name": "task1", "description": "T1"},
            {"name": "task1", "description": "duplicate"},
        ],
    }

    with pytest.raises(ValueError):
        FlowConfigSchema.model_validate(data)


def test_invalid_condition_target():
    data = {
        **BASE,
        "conditions": [
            {
                "name": "cond1",
                "description": "",
                "source_task": "task1",
                "outcome": "success",
                "target_task_success": "does_not_exist",
                "target_task_failure": "end",
            }
        ],
    }

    with pytest.raises(ValueError):
        FlowConfigSchema.model_validate(data)


def test_duplicate_condition_name():
    data = {
        **BASE,
        "tasks": [
            {"name": "task1", "description": "T1"},
            {"name": "task2", "description": "T2"},
            {"name": "task3", "description": "T3"},
        ],
        "conditions": [
            {
                "name": "cond1",
                "description": "",
                "source_task": "task1",
                "outcome": "success",
                "target_task_success": "task2",
                "target_task_failure": "end",
            },
            {
                "name": "cond1",
                "description": "",
                "source_task": "task2",
                "outcome": "success",
                "target_task_success": "task3",
                "target_task_failure": "end",
            },
        ],
    }

    with pytest.raises(ValueError):
        FlowConfigSchema.model_validate(data)
