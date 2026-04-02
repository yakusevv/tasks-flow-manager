from enum import StrEnum
from typing import Any

from pydantic import BaseModel


class TaskOutcomeEnum(StrEnum):
    SUCCESS = "success"
    FAILURE = "failure"


class FlowOutcomeEnum(StrEnum):
    COMPLETED = "completed"
    ENDED_EARLY = "ended_early"
    FAILED = "failed"


class TaskConfigSchema(BaseModel):
    name: str
    description: str


class ConditionConfigSchema(BaseModel):
    name: str
    description: str
    source_task: str
    outcome: TaskOutcomeEnum
    target_task_success: str  # task name or "end"
    target_task_failure: str  # task name or "end"


class FlowConfigSchema(BaseModel):
    id: str
    name: str
    start_task: str
    tasks: list[TaskConfigSchema]
    conditions: list[ConditionConfigSchema]


class TaskResultSchema(BaseModel):
    task_name: str
    outcome: TaskOutcomeEnum
    data: Any = None
    error: str | None = None


class FlowContextSchema(BaseModel):
    flow_id: str
    results: dict[str, TaskResultSchema] = {}


class FlowRunResultSchema(BaseModel):
    flow_id: str
    completed_tasks: list[str]
    final_outcome: FlowOutcomeEnum
    errors: list[str] = []
