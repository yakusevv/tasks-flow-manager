from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from api.api_v1.api import api as api_v1
from core.config import Settings
from core.flow_loader import FlowLoader
from core.logging import configure_logging
from core.mongo_flow_loader import MongoFlowLoader

configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = Settings()
    if settings.mongodb_uri:
        client: AsyncIOMotorClient[dict] = AsyncIOMotorClient(settings.mongodb_uri)
        try:
            await client.admin.command("ping")
        except Exception as exc:
            raise RuntimeError(f"Failed to connect to MongoDB: {exc}") from exc
        collection = client[settings.mongodb_db][settings.mongodb_collection]
        app.state.flow_loader = MongoFlowLoader(collection)
        try:
            yield
        finally:
            client.close()
    else:
        app.state.flow_loader = FlowLoader()
        yield


app = FastAPI(title="Flow Manager", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def healthcheck():
    """Simple health check endpoint."""
    return {"status": "ok"}


app.include_router(api_v1)
