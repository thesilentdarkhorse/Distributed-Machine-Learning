import socket
import threading
from protocol import serialize, deserialize

HOST = '192.168.1.103'
PORT = 9090


class SocketClient:
    def __init__(self, HOST: str, PORT: int) -> None:
        self.HOST = HOST
        self.PORT = PORT
        self.client_socket = None
        self.connected = False

    def server_connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))

        self.connected = True
        print("Client Connected")

        listen_thread = threading.Thread(target=self.listen_loop)
        listen_thread.start()

    def send_message(self, message):
        if not self.connected:
            print("Client not connected")
            return

        data = serialize(message)
        self.client_socket.send(data)

    def receive_message(self):
        try:
            server_message = self.client_socket.recv(1024)

            if not server_message:
                return None

            return deserialize(server_message)

        except:
            return None

    def listen_loop(self):
        while self.connected:
            message = self.receive_message()

            if message is None:
                print("Server disconnected")
                self.close_client()
                break

            print("Server message:", message)

    def close_client(self):
        self.connected = False

        if self.client_socket:
            self.client_socket.close()

        print("Client Closed")

client  = SocketClient(HOST,PORT)
client.server_connect()
client.send_message("Hello")