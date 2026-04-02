import pytest

from models.flow import FlowContextSchema, TaskOutcomeEnum
from tasks.base_task import BaseTask


class SuccessTask(BaseTask):
    name = "success_task"

    async def run(self, context: FlowContextSchema) -> dict:
        return {"key": "value"}


class FailingTask(BaseTask):
    name = "failing_task"

    async def run(self, context: FlowContextSchema) -> dict:
        raise ValueError("something went wrong")


@pytest.fixture
def context() -> FlowContextSchema:
    return FlowContextSchema(flow_id="test")


async def test_base_task_execute_success(context):
    result = await SuccessTask().execute(context)

    assert result.outcome == TaskOutcomeEnum.SUCCESS
    assert result.data == {"key": "value"}
    assert result.error is None


async def test_base_task_execute_exception_becomes_failure(context):
    result = await FailingTask().execute(context)

    assert result.outcome == TaskOutcomeEnum.FAILURE
    assert result.data is None
    assert "something went wrong" in result.error
