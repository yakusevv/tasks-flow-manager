from motor.motor_asyncio import AsyncIOMotorCollection

from core.flow_loader import FlowNotFoundError
from models.flow import FlowConfigSchema


class MongoFlowLoader:
    def __init__(self, collection: AsyncIOMotorCollection) -> None:  # type: ignore[type-arg]
        self._collection = collection

    async def load(self, flow_id: str) -> FlowConfigSchema:
        doc = await self._collection.find_one({"_id": flow_id})
        if doc is None:
            raise FlowNotFoundError(flow_id)
        doc.pop("_id")
        return FlowConfigSchema.model_validate({"id": flow_id, **doc})

    async def list_all(self) -> list[FlowConfigSchema]:
        docs = await self._collection.find().to_list(length=None)
        return [
            FlowConfigSchema.model_validate(
                {"id": doc["_id"], **{k: v for k, v in doc.items() if k != "_id"}}
            )
            for doc in docs
        ]
