from fastapi import APIRouter, HTTPException, status

from core.flow_engine import FlowCycleError, FlowEngine
from core.flow_loader import FlowLoader, FlowNotFoundError
from core.registry import task_registry
from models.flow import FlowConfigSchema, FlowRunResultSchema

router = APIRouter()
flow_loader = FlowLoader()


@router.get("/flows", response_model=list[FlowConfigSchema])
async def list_flows():
    """List all available flows."""
    return flow_loader.list_all()


@router.post("/flows/{flow_id}/run", response_model=FlowRunResultSchema)
async def run_flow(flow_id: str):
    """Run a flow by its ID."""
    try:
        config = flow_loader.load(flow_id)
    except FlowNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

    try:
        engine = FlowEngine(config=config, registry=task_registry)
        return await engine.run()
    except FlowCycleError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
