from project.protocol import Protocol
import socket
import _thread as thread
from project.server import *


#  opens 2022 port and receives messages from server asynchronously

class Messenger:
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    port = Protocol.env_vars["messenger_port"]

    @classmethod
    def start_receiving(cls, client):
        #  send data to server about messenger activity and let check
        server = Server
        # print(cls.IPAddr)

        server.host = cls.hostname
        server.port = cls.port
        s = server.create_socket(False)
        thread.start_new_thread(cls.recieve_message, (client,s))
        return s
        # print("oute form receiving")

    @classmethod
    def recieve_message(cls, s):
        try:

            while True:
                # Establish connection with client.
                c, addr = s.accept()
                print(cls.receive_message_from_client(c))
        except Exception as e:
            print("Messager error occured: " )
            print(e)

    @classmethod
    def send_message(cls, sender, receiver, users_data, message: str):
        resp = ' ___ '
        if sender in users_data:
            if receiver in users_data:
                s = socket.socket()

                # Define the port on which you want to connect

                # connect to the server on local computer
                s.connect((users_data[receiver]["addr"][0], cls.port))
                resp = cls.send_socket_message(message, Protocol.commands["send"], s)
                s.close()
            else:
                resp = "receiver not found"
        else:
            resp = "sender not defined !"
        return resp

    @classmethod
    def receive_message_from_client(cls, conn):
        # msg = cls.recvallMine(conn)
        msg = conn.recv(1024)
        print("messenger receiver some message")
        print(msg)
        print("+++++++++++++++++++++++++")
        # data_loaded = pickle.loads(msg.encode(Protocol.message_encoding))
        msg = Protocol.message_decoder(msg, conn)
        if msg["command"] == Protocol.commands["send"]:
            message = msg["data"]
        else:
            print("messenger receiver not send  command")
            print(msg)
            print("+++++++++++++++++++++++++")
            message = "messenger receiver not send  command"

        return message

    @classmethod
    def send_socket_message(cls, data, command: str, socket):
        payload = Protocol.format_payload(data, command)
        payload = Protocol.message_encoder(payload, command, 2)
        msg = Protocol.message_encoder(payload, command)
        # print("_____________client payload")
        # print(payload)
        # print("________________")
        # print(msg)
        # cls.users_data_client["socket"].sendall(bytes(data_string, encoding=Protocol.message_encoding))
        socket.sendall(msg)
        return cls.receive_message_from_client(socket)
