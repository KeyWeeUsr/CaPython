import json
from enum import Enum
from os import environ
from traceback import format_exc
from uuid import uuid4

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

# config vars
CAPYTHON_SCRIPT_ENTRYPOINT = environ.get("CAPYTHON_SCRIPT_ENTRYPOINT")
CAPYTHON_BASE_URL = environ.get(
    "CAPYTHON_BASE_URL", "http://camunda:8080/engine-rest"
)
CAPYTHON_TOPIC_SEPARATOR = ","
CAPYTHON_TOPICS = environ.get(
    "CAPYTHON_TOPICS".split(CAPYTHON_TOPIC_SEPARATOR), ["topic"]
)
CAPYTHON_ID = environ.get("CAPYTHON_ID", str(uuid4()))


class Topic(Enum):
    topic = "topic"


class BpmnException(Exception):
    def __init__(self, code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bpmn_code = code


def serialize(item):
    default = f"(unserializable) {repr(item)}"
    if isinstance(item, type("dummy", (), {})):
        return f"I'm {item}, handle me, somehow"
    return default


def prepare_vars(task):
    variables = task.get_variables()
    variables["BpmnException"] = BpmnException
    variables["__task__"] = task
    return variables


def clean_vars(variables):
    if "__builtins__" in variables:
        del variables["__builtins__"]
        del variables["BpmnException"]
        del variables["__task__"]


def serialize_vars(variables):
    return json.loads(json.dumps(variables, default=serialize))


def execute(task: ExternalTask):
    try:
        variables = prepare_vars(task)
        exec(variables.get(CAPYTHON_SCRIPT_ENTRYPOINT, "") or "", variables)

        # clean trash in globals
        clean_vars(variables)

        variables = serialize_vars(variables)
        return task.complete(variables)

    except Exception as exc:
        formatted = format_exc()

        clean_vars(variables)
        variables = serialize_vars(variables)

        if isinstance(exc, BpmnException):
            return task.bpmn_error(
                error_code=str(exc.bpmn_code), error_message=formatted,
                variables=variables
            )
        return task.failure(
            error_message="Python Exception",  error_details=formatted,
            max_retries=0, retry_timeout=0
        )


def handler(task: ExternalTask) -> TaskResult:
    topic = task.get_topic_name()
    task_id = task.get_task_id()

    if topic == Topic.topic.value:
        return execute(task)


if __name__ == '__main__':
    worker = ExternalTaskWorker(
        worker_id=CAPYTHON_ID, base_url=CAPYTHON_BASE_URL,
        config=DEFAULT_CONFIG
    )
    worker.subscribe(CAPYTHON_TOPICS, handler)
