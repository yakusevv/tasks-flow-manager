from models.flow import FlowContextSchema
from tasks.base_task import BaseTask


class FetchDataTask(BaseTask):
    name = "task1"

    async def run(self, context: FlowContextSchema) -> dict:
        # Simulate fetching data from an external source
        data = {"records": [{"id": 1, "value": "foo"}, {"id": 2, "value": "bar"}]}
        return data
