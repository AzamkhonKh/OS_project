# Import socket module
import socket
from helper import env_vars, console_line

host = env_vars['client_host']
port = env_vars['server_listening_port']


def sendMessage(socket, input_message: str = "input something: "):
    message = input(input_message)
    # while message != env_vars["exit_word"]:
    socket.send(message.encode())
    return socket.recv(1024).decode()


def test(host, port):
    # Create a socket object
    s = socket.socket()

    # Define the port on which you want to connect

    # connect to the server on local computer
    s.connect((host, port))
    #  there serever should say smth like hey i see you clien
    #  if this not happens smth went wrong
    print(s.recv(1024).decode())
    print("__________")
    # receive data from the server and decoding to get the string.
    # close the connection
    console_line(sendMessage, s, "send something to server: ")
    s.close()
