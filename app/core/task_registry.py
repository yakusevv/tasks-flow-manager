import logging

from tasks.base_task import BaseTask

logger = logging.getLogger(__name__)


class TaskNotFoundError(Exception):
    def __init__(self, task_name: str) -> None:
        self.task_name = task_name
        super().__init__(f"Task '{task_name}' is not registered")


class TaskRegistry:
    def __init__(self) -> None:
        self._registry: dict[str, BaseTask] = {}

    def register(self, task: BaseTask) -> None:
        logger.debug(f'Registering task "{task.name}"')
        self._registry[task.name] = task

    def get(self, task_name: str) -> BaseTask:
        task = self._registry.get(task_name)
        if task is None:
            raise TaskNotFoundError(task_name)
        return task

    def all(self) -> list[BaseTask]:
        return list(self._registry.values())
