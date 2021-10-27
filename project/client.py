import sys
import socket
from project.messenger import Messenger
from project.helper import *
from project.protocol import Protocol


class Client:
    host = env_vars['client_host']
    port = env_vars['server_listening_port']
    msg = Messenger
    users_data_client = dict()

    @classmethod
    def sendMessageClient(cls, input_message: str = "input something: "):
        message = input(input_message)
        if len(message) > 0:
            # while message != env_vars["exit_word"]:
            cls.send_socket_message(message)
            return cls.receive_message(Protocol.commands["MESSAGE"])
        else:
            return cls.sendMessageClient("input something valid to send to server: ")

    @classmethod
    def test(cls, username: str):
        # Create a socket object
        s = socket.socket()

        # Define the port on which you want to connect

        # connect to the server on local computer
        s.connect((cls.host, cls.port))

        cls.users_data_client = {
            "name": username,
            "socket": s,
            "type": "client"
        }
        cls.send_socket_message(username, Protocol.commands["AUTH"])

        #  there serever should say smth like hey i see you clien
        #  if this not happens smth went wrong
        print(cls.receive_message(Protocol.commands["AUTH"]))
        print("__________")
        # receive data from the server and decoding to get the string.
        # close the connection

        # cls.msg.recieve_message(cls)

        console_line(cls.sendMessageClient, cls.users_data_client, "send something to server: ")
        sys.exit()

    # received and sending as well message struct
    # {
    #     "message": "related comment or protocol command"
    #     "data": {
    #         "some data "
    #     }
    #      "code":  --- this line may be in future
    # }
    @classmethod
    def send_socket_message(cls, data, command: str = Protocol.commands["MESSAGE"]):
        payload = format_payload(data, command)
        payload = message_encoder(payload, command, 2)
        msg = message_encoder(payload, command)
        # cls.users_data_client["socket"].sendall(bytes(data_string, encoding=Protocol.message_encoding))
        cls.users_data_client["socket"].sendall(msg)

    @classmethod
    def receive_message(cls, command: str = Protocol.commands["MESSAGE"], userSocket=None):
        #  this should be Json with
        # msg = cls.users_data_client["socket"].recv(1024).decode(Protocol.message_encoding)
        if userSocket is None:
            userSocket = cls.users_data_client["socket"]
        msg = userSocket.recv(1024)
        # data_loaded = pickle.loads(msg.encode(Protocol.message_encoding))
        msg = message_decoder(msg)
        # print(msg)
        if command == Protocol.commands["MESSAGE"]:
            return msg['data']['message']
        else:
            return msg['data']

        # if msg != '':
        #     print("received before decode" + loads)
        #     print(loads)
