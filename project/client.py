import json
import sys
import socket
from project.messenger import Messenger
from project.helper import env_vars, console_line
from project.protocol import Protocol


class Client:
    host = env_vars['client_host']
    port = env_vars['server_listening_port']
    msg = Messenger
    users_data_client = dict()

    @classmethod
    def sendMessageClient(cls, user_data, input_message: str = "input something: "):
        socketUser = user_data["socket"]
        message = input(input_message)
        if len(message) > 0:
            # while message != env_vars["exit_word"]:
            socketUser.send(message.encode())
            return socketUser.recv(1024).decode()
        else:
            return cls.sendMessageClient(user_data, "input something valid to send to server: ")

    @classmethod
    def test(cls, username: str):
        # Create a socket object
        s = socket.socket()

        # Define the port on which you want to connect

        # connect to the server on local computer
        s.connect((cls.host, cls.port))
        msg = username
        cls.send_socket_message(msg, "AUTH")

        cls.users_data_client = {
            "name": username,
            "socket": s,
            "type": "client"
        }
        #  there serever should say smth like hey i see you clien
        #  if this not happens smth went wrong
        print(cls.receive_message())
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
        if data is str:
            payload = {"message": data}
        else:
            payload = data
        msg = {
            "message": command,
            "data": {
                payload
            }
        }

        data_string = json.dumps(msg, indent=Protocol.ident_in_message)
        cls.users_data_client["socket"].send(data_string.encode())

    @classmethod
    def receive_message(cls):
        #  this should be json with
        msg = cls.users_data_client["socket"].recv(1024).decode()
        data_loaded = json.loads(msg)
        print(data_loaded)
