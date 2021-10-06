from enum import Enum
from traceback import format_exc

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


class BpmnException(Exception):
    def __init__(self, code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bpmn_code = code


def execute(task: ExternalTask):
    try:
        variables = task.get_variables()
        variables["BpmnException"] = BpmnException

        exec(variables.get("python", ""), variables)

        # clean trash in globals
        if "__builtins__" in variables:
            del variables["__builtins__"]

        return task.complete(variables)

    except Exception as exc:
        formatted = format_exc()
        if isinstance(exc, BpmnException):
            return task.bpmn_error(
                error_code=str(exc.bpmn_code), error_message=formatted,
                variables=variables
            )
        return task.failure(
            error_message="Python Exception",  error_details=format_exc(),
            max_retries=0, retry_timeout=0
        )


def handler(task: ExternalTask) -> TaskResult:
    topic = task.get_topic_name()
    task_id = task.get_task_id()

    if topic == Topic.topic.value:
        return execute(task)


if __name__ == '__main__':
    worker = ExternalTaskWorker(
        worker_id="1", base_url="http://camunda:8080/engine-rest",
        config=DEFAULT_CONFIG
    )
    worker.subscribe(["topic"], handler)
