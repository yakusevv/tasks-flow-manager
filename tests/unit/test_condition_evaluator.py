import pytest

from core.condition_evaluator import ConditionEvaluator
from models.flow import END, ConditionConfigSchema, TaskOutcomeEnum


def make_condition(
    source: str, on_success: str, on_failure: str
) -> ConditionConfigSchema:
    return ConditionConfigSchema(
        name=f"cond_{source}",
        description="",
        source_task=source,
        outcome=TaskOutcomeEnum.SUCCESS,
        target_task_success=on_success,
        target_task_failure=on_failure,
    )


@pytest.fixture
def evaluator() -> ConditionEvaluator:
    return ConditionEvaluator([make_condition("task1", "task2", END)])


def test_condition_evaluator_success_route(evaluator):
    assert evaluator.next_task("task1", TaskOutcomeEnum.SUCCESS) == "task2"


def test_condition_evaluator_failure_route(evaluator):
    assert evaluator.next_task("task1", TaskOutcomeEnum.FAILURE) == END


def test_condition_evaluator_no_condition_returns_end(evaluator):
    assert evaluator.next_task("unknown_task", TaskOutcomeEnum.SUCCESS) == END
