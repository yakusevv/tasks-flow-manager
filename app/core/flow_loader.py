import asyncio
import json
from pathlib import Path

from models.flow import FlowConfigSchema


FLOWS_FILE = Path(__file__).parent.parent.parent / "config" / "flows.json"


class FlowNotFoundError(Exception):
    def __init__(self, flow_id: str) -> None:
        self.flow_id = flow_id
        super().__init__(f"Flow '{flow_id}' not found in flows.json")


class FlowLoader:
    def __init__(self, flows_file: Path = FLOWS_FILE) -> None:
        self.flows_file = flows_file

    async def _read_all_raw(self) -> dict:
        text = await asyncio.to_thread(self.flows_file.read_text)
        return json.loads(text)

    async def load(self, flow_id: str) -> FlowConfigSchema:
        raw = await self._read_all_raw()
        if flow_id not in raw:
            raise FlowNotFoundError(flow_id)
        return FlowConfigSchema.model_validate({"id": flow_id, **raw[flow_id]})

    async def list_all(self) -> list[FlowConfigSchema]:
        raw = await self._read_all_raw()
        return [
            FlowConfigSchema.model_validate({"id": flow_id, **flow_data})
            for flow_id, flow_data in raw.items()
        ]
