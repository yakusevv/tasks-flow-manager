import asyncio
import json
from pathlib import Path

from core.flows.exceptions import FlowAlreadyExistsError, FlowNotFoundError
from models.flow import FlowConfigSchema


FLOWS_FILE = Path(__file__).parent.parent.parent / "config" / "flows.json"


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

    async def create(self, flow: FlowConfigSchema) -> FlowConfigSchema:
        raw = await self._read_all_raw()
        if flow.id in raw:
            raise FlowAlreadyExistsError(flow.id)
        raw[flow.id] = flow.model_dump(exclude={"id"})
        await asyncio.to_thread(self.flows_file.write_text, json.dumps(raw, indent=2))
        return flow

    async def delete(self, flow_id: str) -> None:
        raw = await self._read_all_raw()
        if flow_id not in raw:
            raise FlowNotFoundError(flow_id)
        del raw[flow_id]
        await asyncio.to_thread(self.flows_file.write_text, json.dumps(raw, indent=2))
