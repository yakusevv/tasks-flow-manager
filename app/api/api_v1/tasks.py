from fastapi import APIRouter

from core.registry import task_registry
from models.flow import TaskInfoSchema

router = APIRouter()


@router.get("/tasks", response_model=list[TaskInfoSchema])
async def list_tasks():
    """List all registered tasks."""
    return [TaskInfoSchema(name=task.name) for task in task_registry.all()]
