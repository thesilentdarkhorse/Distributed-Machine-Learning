import time

class WorkerRegistry:

    def __init__(self):
        self.workers = {}

    def register_worker(self, worker_id, socket):
        self.workers[worker_id] = {
            "socket":socket,
            "status":"idle",
            "last_heartbeat": time.time(),
            "task": None
            }


    def remove_worker(self, worker_id):
        if worker_id in self.workers:
            self.workers.pop(worker_id)
            print(f"Removed worker {worker_id}")

    def update_heartbeat(self, worker_id):
        if worker_id in self.workers:
            self.workers[worker_id]["last_heartbeat"] = time.time()


    def get_available_worker(self):
        for worker_id, info in self.workers.items():
            if info["status"] == "idle":
                return worker_id
        return None



    def assign_task(self, worker_id, task):
        if worker_id in self.workers:
            self.workers[worker_id]["status"] = "busy"
            self.workers[worker_id]["task"] = task

    def complete_task(self, worker_id):
        if worker_id in self.workers:
            self.workers[worker_id]["status"] = "idle"
            self.workers[worker_id]["task"] = None

    def get_worker_socket(self, worker_id):
        if worker_id in self.workers:
            return self.workers[worker_id]["socket"]
        else:
            return None
        

    def list_workers(self):
        return self.workers
    
    