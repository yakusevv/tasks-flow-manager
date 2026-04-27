import logging

from models.flow import ConditionConfigSchema, TaskOutcomeEnum, END

logger = logging.getLogger(__name__)


class ConditionEvaluator:
    def __init__(self, conditions: list[ConditionConfigSchema]) -> None:
        self._conditions: dict[str, ConditionConfigSchema] = {
            c.source_task: c for c in conditions
        }

    def next_task(self, task_name: str, outcome: TaskOutcomeEnum) -> str:
        condition = self._conditions.get(task_name)

        if condition is None:
            logger.debug(f'No condition for task "{task_name}", ending flow')
            return END

        next_task = (
            condition.target_task_success
            if outcome == TaskOutcomeEnum.SUCCESS
            else condition.target_task_failure
        )

        logger.debug(
            f'Task "{task_name}" outcome="{outcome}" → next task: "{next_task}"'
        )
        return next_task
