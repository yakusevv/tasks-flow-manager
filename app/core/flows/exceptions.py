class FlowNotFoundError(Exception):
    def __init__(self, flow_id: str) -> None:
        self.flow_id = flow_id
        super().__init__(f"Flow '{flow_id}' not found")


class FlowCycleError(Exception):
    def __init__(self, task_name: str) -> None:
        super().__init__(
            f"Cycle detected: task '{task_name}' has already been executed"
        )
