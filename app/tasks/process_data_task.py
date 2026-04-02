import logging

from models.flow import FlowContextSchema, TaskOutcomeEnum
from tasks.base_task import BaseTask

logger = logging.getLogger(__name__)


class ProcessDataTask(BaseTask):
    name = "task2"
    _fetch_tasks = ["task1"]

    async def run(self, context: FlowContextSchema) -> dict:
        records: list = []
        for fetch_task in self._fetch_tasks:
            fetch_result = context.results.get(fetch_task)
            if fetch_result is None or fetch_result.outcome != TaskOutcomeEnum.SUCCESS:
                continue

            records += fetch_result.data.get("records", [])

        if not records:
            logger.warning(
                "No records to process — all source tasks failed or returned empty"
            )

        # Simulate processing data (e.g. transforming or analyzing records)
        processed = [{"id": r["id"], "value": r["value"].upper()} for r in records]
        return {"processed_records": processed}
