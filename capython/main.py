import json
from enum import Enum
from os import environ
from traceback import format_exc
from uuid import uuid4

from camunda.external_task.external_task import ExternalTask, TaskResult
from camunda.external_task.external_task_worker import ExternalTaskWorker

# config vars
CAPYTHON_SCRIPT_ENTRYPOINT = environ.get(
    "CAPYTHON_SCRIPT_ENTRYPOINT", "capython"
)
CAPYTHON_BASE_URL = environ.get(
    "CAPYTHON_BASE_URL", "http://camunda:8080/engine-rest"
)
CAPYTHON_TOPIC_SEPARATOR = ","
CAPYTHON_TOPICS = environ.get(
    "CAPYTHON_TOPICS", "topic"
).split(CAPYTHON_TOPIC_SEPARATOR)
CAPYTHON_ID = environ.get("CAPYTHON_ID", str(uuid4()))

CAPYTHON_MAX_TASKS = int(environ.get("CAPYTHON_MAX_TASKS", 1))
CAPYTHON_LOCK_DURATION = int(environ.get("CAPYTHON_LOCK_DURATION", 10000))
CAPYTHON_ASYNC_RESPONSE_TIMEOUT = int(environ.get(
    "CAPYTHON_ASYNC_RESPONSE_TIMEOUT", 5000
))
CAPYTHON_RETRIES = int(environ.get("CAPYTHON_RETRIES", 3))
CAPYTHON_RETRY_TIMEOUT = int(environ.get("CAPYTHON_RETRY_TIMEOUT", 5000))
CAPYTHON_SLEEP_SECONDS = int(environ.get("CAPYTHON_SLEEP_SECONDS", 30))


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
    variables["__task_id__"] = task.get_task_id()
    variables["__topic__"] = task.get_topic_name()
    return variables


def failure_recovery_opts(variables):
    return dict(
        max_retries=int(variables.get("__task_retries__") or 0),
        retry_timeout=int(
            variables.get("__task_retry_timeout__") or CAPYTHON_RETRY_TIMEOUT
        )
    )


def clean_vars(variables):
    known = [
        "__builtins__", "BpmnException", "__task__", "__task_id__",
        "__topic__", "__task_retries__", "__task_retry_timeout__"
    ]
    for var in known:
        if var not in variables:
            continue
        del variables[var]


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
            **failure_recovery_opts(variables)
        )


def handler(task: ExternalTask) -> TaskResult:
    return execute(task)


if __name__ == '__main__':
    worker = ExternalTaskWorker(
        worker_id=CAPYTHON_ID, base_url=CAPYTHON_BASE_URL,
        config={
            "maxTasks": CAPYTHON_MAX_TASKS,
            "lockDuration": CAPYTHON_LOCK_DURATION,
            "asyncResponseTimeout": CAPYTHON_ASYNC_RESPONSE_TIMEOUT,
            "retries": CAPYTHON_RETRIES,
            "retryTimeout": CAPYTHON_RETRY_TIMEOUT,
            "sleepSeconds": CAPYTHON_SLEEP_SECONDS
        }
    )
    worker.subscribe(CAPYTHON_TOPICS, handler)
