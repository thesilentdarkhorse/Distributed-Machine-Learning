#Protocols

REGISTER = "REGISTER"
HEARTBEAT = "HEARTBEAT"
TASK = "TASK"
RESULT = "RESULT"
FAILURE = "FAILURE"

#Helper function

def register_message(worker_id):
    return {
        "type": REGISTER,
        "worker_id": worker_id
    }

def task_message(task_data):
    return {
        "type": TASK,
        "task": task_data
    }

def result_message(worker_id, result):
    return {
        "type": RESULT,
        "worker_id": worker_id,
        "result": result
    }
