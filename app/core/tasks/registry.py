from core.tasks.task_registry import TaskRegistry
from core.tasks.fetch_data_task import FetchDataTask
from core.tasks.process_data_task import ProcessDataTask
from core.tasks.store_data_task import StoreDataTask

task_registry = TaskRegistry()
task_registry.register(FetchDataTask())
task_registry.register(ProcessDataTask())
task_registry.register(StoreDataTask())
