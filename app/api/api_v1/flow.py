from fastapi import APIRouter, HTTPException, status

from core.dependencies import FlowLoaderDep
from core.flows.exceptions import FlowAlreadyExistsError, FlowCycleError, FlowNotFoundError
from core.flows.flow_engine import FlowEngine
from core.tasks.registry import task_registry
from models.flow import FlowConfigSchema, FlowRunResultSchema

router = APIRouter()


@router.get("/flows", response_model=list[FlowConfigSchema])
async def list_flows(flow_loader: FlowLoaderDep):
    """List all available flows."""
    return await flow_loader.list_all()


@router.post("/flows", response_model=FlowConfigSchema, status_code=status.HTTP_201_CREATED)
async def create_flow(flow: FlowConfigSchema, flow_loader: FlowLoaderDep):
    """Create a new flow."""
    try:
        return await flow_loader.create(flow)
    except FlowAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.delete("/flows/{flow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_flow(flow_id: str, flow_loader: FlowLoaderDep):
    """Delete a flow by its ID."""
    try:
        await flow_loader.delete(flow_id)
    except FlowNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/flows/{flow_id}/run", response_model=FlowRunResultSchema)
async def run_flow(flow_id: str, flow_loader: FlowLoaderDep):
    """Run a flow by its ID."""
    try:
        config = await flow_loader.load(flow_id)
    except FlowNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

    try:
        engine = FlowEngine(config=config, registry=task_registry)
        return await engine.run()
    except FlowCycleError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
