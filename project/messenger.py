from project.server import Server
from project.helper import env_vars
import socket


#  opens 2022 port and receives messages from server asynchronously

class Messenger:
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    port = env_vars["messenger_port"]

    @classmethod
    def recieve_message(cls, client):
        try:
            #  send data to server about messenger activity and let check
            if client.users_data_client["type"] == "client":
                sock = client.users_data_client["socket"]
                sock.send("this is from messenger".encode())
                print(sock.recv(1024).decode())

            server = Server
            server.host = cls.hostname
            server.port = cls.port
            server.start_server()
        except Exception as e:
            print("Messager error occured: " + e)

    @classmethod
    def send_message(cls, sender, receiver, users_data, message: str):
        if sender in users_data:
            if receiver in users_data:
                users_data[receiver]["messages"]["connection"].send(message.encode())
            else:
                print("receiver not found")
        else:
            print("sender not defined !")
