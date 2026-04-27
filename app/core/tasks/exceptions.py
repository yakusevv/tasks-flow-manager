class TaskNotFoundError(Exception):
    def __init__(self, task_name: str) -> None:
        self.task_name = task_name
        super().__init__(f"Task '{task_name}' is not registered")
