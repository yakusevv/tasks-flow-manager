from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, model_validator


END = "end"


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

    @model_validator(mode="after")
    def validate_flow(self) -> "FlowConfigSchema":
        errors: list[str] = []
        task_names: set[str] = {t.name for t in self.tasks}
        valid_targets = task_names | {END}

        if self.start_task not in task_names:
            errors.append(
                f"start_task '{self.start_task}' does not match any task name"
            )

        seen_tasks: set[str] = set()
        for task in self.tasks:
            if task.name in seen_tasks:
                errors.append(f"Duplicate task name: '{task.name}'")
            seen_tasks.add(task.name)

        seen_conditions: set[str] = set()
        for condition in self.conditions:
            if condition.name in seen_conditions:
                errors.append(f"Duplicate condition name: '{condition.name}'")
            seen_conditions.add(condition.name)

            if condition.source_task not in task_names:
                errors.append(
                    f"Condition '{condition.name}': source_task '{condition.source_task}' "
                    "does not match any task"
                )
            if condition.target_task_success not in valid_targets:
                errors.append(
                    f"Condition '{condition.name}': target_task_success "
                    f"'{condition.target_task_success}' does not match any task or 'end'"
                )
            if condition.target_task_failure not in valid_targets:
                errors.append(
                    f"Condition '{condition.name}': target_task_failure "
                    f"'{condition.target_task_failure}' does not match any task or 'end'"
                )

        if errors:
            raise ValueError(errors)

        return self


class TaskResultSchema(BaseModel):
    task_name: str
    outcome: TaskOutcomeEnum
    data: Optional[dict] = None
    error: Optional[str] = None


class FlowContextSchema(BaseModel):
    flow_id: str
    results: dict[str, TaskResultSchema] = {}


class FlowRunResultSchema(BaseModel):
    flow_id: str
    completed_tasks: list[str]
    final_outcome: FlowOutcomeEnum
    errors: list[str] = []
