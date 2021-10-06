from dataclasses import dataclass
from enum import Enum

from camunda.external_task.external_task import ExternalTask, TaskResult
from camunda.external_task.external_task_worker import ExternalTaskWorker


DEFAULT_CONFIG = {
    "maxTasks": 1,
    "lockDuration": 10000,
    "asyncResponseTimeout": 5000,
    "retries": 3,
    "retryTimeout": 5000,
    "sleepSeconds": 30
}

class Topic(Enum):
    topic = "topic"


def execute(code):
    from importlib import import_module
    eval(code, {}, {"import_module": import_module})


def handler(task: ExternalTask) -> TaskResult:
    topic = task.get_topic_name()
    task_id = task.get_task_id()
    

    if topic == Topic.topic.value:
        return execute(task)


if __name__ == '__main_asd_':
    worker = ExternalTaskWorker(worker_id="1", config=DEFAULT_CONFIG)
    worker.subscribe(["topic"], handler)
