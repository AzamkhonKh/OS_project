import sys
import socket
from helper import env_vars, console_line

host = env_vars['client_host']
port = env_vars['server_listening_port']

users_data_client = dict()

def sendMessageClient(user_data, input_message: str = "input something: "):
    socketUser = user_data["socket"]
    message = input(input_message)
    # while message != env_vars["exit_word"]:
    socketUser.send(message.encode())
    return socketUser.recv(1024).decode()


def test(username: str, host, port):
    # Create a socket object
    s = socket.socket()

    # Define the port on which you want to connect

    # connect to the server on local computer
    s.connect((host, port))
    msg = "username: " + username
    s.send(msg.encode())


    users_data_client = {
        "name": username,
        "socket": s,
        "type": "client"
    }
    #  there serever should say smth like hey i see you clien
    #  if this not happens smth went wrong
    print(s.recv(1024).decode())
    print("__________")
    # receive data from the server and decoding to get the string.
    # close the connection
    console_line(sendMessageClient, users_data_client, "send something to server: ")
    sys.exit()
