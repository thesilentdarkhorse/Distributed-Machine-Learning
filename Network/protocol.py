import json


REGISTER = "REGISTER"
HEARTBEAT = "HEARTBEAT"
TASK = "TASK"
RESULT = "RESULT"
FAILURE = "FAILURE"


def serialize(message):
    return json.dumps(message).encode("utf-8")

def deserialize(message):
    return json.loads(message.decode("utf-8"))


def register_message(worker_id):
    return {"type": REGISTER, "worker_id": worker_id}


def task_message(worker_id, task_data):
    return {"type": TASK, "worker_id": worker_id, "task": task_data}


def result_message(worker_id, result):
    return {"type": RESULT, "worker_id": worker_id, "result": result}


def heartbeat_message(worker_id):
    return {"type": HEARTBEAT, "worker_id": worker_id}


def failure_message(worker_id, reason):
    return {"type": FAILURE, "worker_id": worker_id, "reason": reason}