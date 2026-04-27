from abc import ABC, abstractmethod
from typing import Optional

from models.flow import FlowContextSchema, TaskOutcomeEnum, TaskResultSchema


class BaseTask(ABC):
    name: str

    async def execute(self, context: FlowContextSchema) -> TaskResultSchema:
        try:
            data = await self.run(context)
            return TaskResultSchema(
                task_name=self.name,
                outcome=TaskOutcomeEnum.SUCCESS,
                data=data,
            )
        except Exception as exc:
            return TaskResultSchema(
                task_name=self.name,
                outcome=TaskOutcomeEnum.FAILURE,
                error=str(exc),
            )

    @abstractmethod
    async def run(self, context: FlowContextSchema) -> Optional[dict]:
        """Execute the task logic. Raise an exception to signal failure."""
