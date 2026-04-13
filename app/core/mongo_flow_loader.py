from motor.motor_asyncio import AsyncIOMotorCollection

from core.flow_loader import FlowNotFoundError
from models.flow import FlowConfigSchema

_MAX_FLOWS = 1000


class MongoFlowLoader:
    def __init__(self, collection: AsyncIOMotorCollection) -> None:  # type: ignore[type-arg]
        self._collection = collection

    def _doc_to_schema(self, doc: dict) -> FlowConfigSchema:
        flow_id = doc["_id"]
        return FlowConfigSchema.model_validate(
            {"id": flow_id, **{k: v for k, v in doc.items() if k != "_id"}}
        )

    async def load(self, flow_id: str) -> FlowConfigSchema:
        doc = await self._collection.find_one({"_id": flow_id})
        if doc is None:
            raise FlowNotFoundError(flow_id)
        return self._doc_to_schema(doc)

    async def list_all(self) -> list[FlowConfigSchema]:
        docs = await self._collection.find().to_list(length=_MAX_FLOWS)
        return [self._doc_to_schema(doc) for doc in docs]
