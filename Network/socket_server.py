import socket
import threading
from protocol import deserialize, serialize, REGISTER, RESULT, HEARTBEAT
from Cluster.worker_registry import WorkerRegistry


HOST = '192.168.1.103'
PORT = 9090


class SocketServer:
    def __init__(self, HOST: str, PORT: int) -> None:
        self.HOST = HOST
        self.PORT = PORT
        self.server_socket = None
        self.clients_list = []
        self.running = False
        self.registry=WorkerRegistry()

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()

        self.running = True
        print("Server Listening")
        self.accept_connections()

    def accept_connections(self):
        while self.running:
            comm_socket, address = self.server_socket.accept()
            print(f"{address} is connected")

            self.clients_list.append(comm_socket)

            thread = threading.Thread(
                target=self.handle_client,
                args=(comm_socket,)
            )
            thread.start()

    def handle_client(self, comm_socket):
        while True:
            message = self.receive_message(comm_socket)

            if message is None:
                self.close_client(comm_socket)
                break

            message = deserialize(message)

            msg_type = message["type"]

            if msg_type == REGISTER:
                worker_id = message["worker_id"]
                self.registry.register_worker(worker_id,comm_socket)

            elif msg_type == RESULT:
                worker_id = message["worker_id"]
                result = message["result"]
                self.registry.complete_task(worker_id)

            elif msg_type == HEARTBEAT:
                worker_id = message["worker_id"]
                self.registry.update_heartbeat(worker_id)

    def receive_message(self, comm_socket):
        try:
            client_message = comm_socket.recv(1024)
            if not client_message:
                return None
            return client_message
        except:
            return None

    def send_message(self, comm_socket, message_dict):
        data = serialize(message_dict)
        comm_socket.send(data)

    def close_client(self, comm_socket):
        comm_socket.close()
        self.clients_list.remove(comm_socket)
        print("Client Disconnected")

    def close_server(self):
        self.running = False

        while self.clients_list:
            self.close_client(self.clients_list[0])

        self.server_socket.close()
        print("Server Closed")


server = SocketServer(HOST, PORT)
server.start_server()