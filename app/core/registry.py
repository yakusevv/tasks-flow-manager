from core.task_registry import TaskRegistry
from tasks.fetch_data_task import FetchDataTask
from tasks.process_data_task import ProcessDataTask
from tasks.store_data_task import StoreDataTask

task_registry = TaskRegistry()
task_registry.register(FetchDataTask())
task_registry.register(ProcessDataTask())
task_registry.register(StoreDataTask())
