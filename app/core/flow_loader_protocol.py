from typing import Protocol

from models.flow import FlowConfigSchema


class FlowLoaderProtocol(Protocol):
    async def load(self, flow_id: str) -> FlowConfigSchema: ...
    async def list_all(self) -> list[FlowConfigSchema]: ...
