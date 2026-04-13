import json

import pytest

from core.flow_loader import FlowLoader, FlowNotFoundError
from models.flow import FlowConfigSchema

VALID_FLOWS = {
    "flow1": {
        "name": "Flow One",
        "start_task": "task1",
        "tasks": [
            {"name": "task1", "description": "Task 1"},
        ],
        "conditions": [],
    }
}


@pytest.fixture
def flows_file(tmp_path):
    f = tmp_path / "flows.json"
    f.write_text(json.dumps(VALID_FLOWS))
    return f


async def test_flow_loader_load_valid_flow(flows_file):
    # given
    loader = FlowLoader(flows_file=flows_file)

    # when
    config = await loader.load("flow1")

    # then
    assert isinstance(config, FlowConfigSchema)
    assert config.id == "flow1"
    assert config.name == "Flow One"


async def test_flow_loader_load_not_found_raises(flows_file):
    # given
    loader = FlowLoader(flows_file=flows_file)

    # when
    with pytest.raises(FlowNotFoundError) as exc_info:
        await loader.load("nonexistent")

    # then
    assert "nonexistent" in str(exc_info.value)


async def test_flow_loader_list_all(flows_file):
    # given
    loader = FlowLoader(flows_file=flows_file)

    # when
    all_flows = await loader.list_all()

    # then
    assert len(all_flows) == 1
    assert all_flows[0].id == "flow1"
