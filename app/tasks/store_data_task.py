import logging

from models.flow import FlowContextSchema, TaskOutcomeEnum
from tasks.base_task import BaseTask

logger = logging.getLogger(__name__)


class StoreDataTask(BaseTask):
    name = "task3"
    _process_tasks = ["task2"]

    async def run(self, context: FlowContextSchema) -> dict:
        records: list = []
        for process_task in self._process_tasks:
            process_result = context.results.get(process_task)
            if (
                process_result is None
                or process_result.outcome != TaskOutcomeEnum.SUCCESS
            ):
                continue

            records += process_result.data.get("processed_records", [])

        if not records:
            logger.warning(
                "No records to store — all source tasks failed or returned empty"
            )

        # Simulate storing data (e.g. writing to a database or file)
        return {"stored_count": len(records), "status": "ok"}
