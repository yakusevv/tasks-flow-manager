from fastapi import APIRouter, HTTPException

from models.flow import FlowRunResultSchema


router = APIRouter()


@router.post("/flows/{flow_id}/run", response_model=FlowRunResultSchema)
async def run_flow(flow_id: str):
    """Endpoint to run a flow by its ID."""
    raise HTTPException(status_code=501, detail="FlowEngine not yet implemented")
