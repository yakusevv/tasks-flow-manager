from fastapi import APIRouter
from api.api_v1 import flow, tasks

api = APIRouter(prefix="/v1")

api.include_router(flow.router)
api.include_router(tasks.router)
