import logging

from core.condition_evaluator import ConditionEvaluator
from core.task_registry import TaskRegistry
from models.flow import (
    END,
    FlowConfigSchema,
    FlowContextSchema,
    FlowOutcomeEnum,
    FlowRunResultSchema,
    TaskOutcomeEnum,
)

logger = logging.getLogger(__name__)


class FlowCycleError(Exception):
    def __init__(self, task_name: str) -> None:
        super().__init__(
            f"Cycle detected: task '{task_name}' has already been executed"
        )


class FlowEngine:
    def __init__(self, config: FlowConfigSchema, registry: TaskRegistry) -> None:
        self.config = config
        self.registry = registry
        self.evaluator = ConditionEvaluator(config.conditions)

    async def run(self) -> FlowRunResultSchema:
        logger.info(f"Starting flow '{self.config.name}' ({self.config.id})")

        context = FlowContextSchema(flow_id=self.config.id)
        current_task_name = self.config.start_task
        completed_tasks: list[str] = []
        visited: set[str] = set()
        errors: list[str] = []

        while current_task_name != END:
            if current_task_name in visited:
                raise FlowCycleError(current_task_name)

            visited.add(current_task_name)

            task = self.registry.get(current_task_name)
            logger.info(f"Executing task '{current_task_name}'")

            result = await task.execute(context)
            context.results[current_task_name] = result
            completed_tasks.append(current_task_name)

            if result.outcome == TaskOutcomeEnum.FAILURE:
                logger.warning(f"Task '{current_task_name}' failed: {result.error}")
                errors.append(f"{current_task_name}: {result.error}")

            current_task_name = self.evaluator.next_task(
                current_task_name, result.outcome
            )

        all_succeeded = all(
            r.outcome == TaskOutcomeEnum.SUCCESS for r in context.results.values()
        )
        final_outcome = (
            FlowOutcomeEnum.COMPLETED if all_succeeded else FlowOutcomeEnum.ENDED_EARLY
        )

        logger.info(
            f"Flow '{self.config.id}' finished — outcome: {final_outcome}, tasks completed: {completed_tasks}"
        )

        return FlowRunResultSchema(
            flow_id=self.config.id,
            completed_tasks=completed_tasks,
            final_outcome=final_outcome,
            errors=errors,
        )
