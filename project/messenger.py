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

        server.host = cls.IPAddr
        server.port = cls.port
        s = server.create_socket(False)
        thread.start_new_thread(cls.recieve_message, (s,))
        return s
        # print("oute form receiving")

    @classmethod
    def recieve_message(cls, s):
        try:

            while True:
                # Establish connection with client.
                # print(s)
                c, addr = s.accept()
                # msg = c.recv(1024)
                # print(msg)
                print(cls.receive_message_from_client(c))
        except Exception as e:
            print("Messager error occured: ")
            print(e)

    @classmethod
    def send_message(cls, sender, receiver, users_data, message: str):
        resp = ' ___ '
        if sender in users_data:
            if receiver in users_data:
                s = socket.socket()

                # Define the port on which you want to connect

                # connect to the server on local computer
                data = dict({
                    "message": message,
                    "from": sender,
                    "to": receiver
                })
                s.connect((users_data[receiver]["messanger"]["addr_ip"], cls.port))
                resp = cls.send_socket_message(data, Protocol.commands["send"], s)
                s.close()
            else:
                resp = "receiver not found"
        else:
            resp = "sender not defined !"
        return resp

    @classmethod
    def receive_message_from_client(cls, conn):
        msg = conn.recv(1024)
        # data_loaded = pickle.loads(msg.encode(Protocol.message_encoding))
        msg = Protocol.message_decoder(msg, conn)
        message = ''
        command = msg["command"]
        # print("messenger receiver some message")
        # print(msg)
        # print("+++++++++++++++++++++++++")
        if command == Protocol.commands["send"]:
            data = msg["data"]
            message += "\n______________\n"
            message += 'message -- "' + data["message"] + '" \n'
            message += 'from -- "' + data["from"] + '" \n'
            message += 'to --  "' + data["to"] + '" \n'
            message += "\n______________\n"

        elif command == Protocol.commands["MESSAGE"]:
            return msg['data']['message']
        else:
            # print("messenger receiver not send  command")
            # print(msg)
            # print("+++++++++++++++++++++++++")
            message = "messenger receiver not send  command"

        cls.send_message_once("recieved OK", Protocol.commands["MESSAGE"], conn)
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

    @classmethod
    def send_message_once(cls, data, command: str, socket):
        payload = Protocol.format_payload(data, command)
        payload = Protocol.message_encoder(payload, command, 2)
        msg = Protocol.message_encoder(payload, command)
        # print("_____________client payload")
        # print(payload)
        # print("________________")
        # print(msg)
        # cls.users_data_client["socket"].sendall(bytes(data_string, encoding=Protocol.message_encoding))
        socket.sendall(msg)
