import socket
import threading

HOST = '192.168.1.103'
PORT=9090

class SocketServer:
    def __init__(self,HOST:str,PORT:int)->None:
        self.HOST = HOST
        self.PORT = PORT
        self.server_socket = None
        self.clients_list = []
        self.running = False
    
    def start_server(self,):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST,self.PORT))
        self.server_socket.listen()
        
        self.running = True
        print("Server Listenting")
        self.accept_connections()
    
    def accept_connections(self):
        while self.running:
            comm_socket,address = self.server_socket.accept()
            print(f"{address} is connected")
            self.clients_list.append(comm_socket)

            thread = threading.Thread(target=self.handle_client,args=(comm_socket,))
            thread.start()

    def handle_client(self,comm_socket):
        while True:
            client_message = self.receive_message(comm_socket)
            if client_message is None:
                self.close_client(comm_socket)
                break
            else:
                print(f"Message is {client_message}")

            
    def receive_message(self,comm_socket):
        client_message = comm_socket.recv(1024)
        if not client_message:
            return None
        else:
            return client_message.decode('utf-8')
    
    def send_message(self,comm_socket,message):
        serialize = f"{message}".encode()
        comm_socket.send(serialize)

    def close_client(self,comm_socket):
        comm_socket.close()
        self.clients_list.remove(comm_socket)
        print(f"Client Disconnected")
    
    def close_server(self):
        self.running = False
        while self.clients_list:
            self.close_client(self.clients_list[0])
        self.server_socket.close()
        print(f"Server is Closed")

# server = SocketServer(HOST,PORT)
# server.start_server()