# Import socket module
import socket
from helper import env_vars, console_line

host = env_vars['client_host']
port = env_vars['server_listening_port']


# def sendMessage(socket):


def test(host, port):
    # Create a socket object
    s = socket.socket()

    # Define the port on which you want to connect

    # connect to the server on local computer
    s.connect((host, port))
    s.send("something from client".encode())
    # receive data from the server and decoding to get the string.
    message = s.recv(1024).decode()
    while message != "close":
        s.send(message.encode())
        print(message)
        message = input("input something: ")
    # close the connection
    # console_line("send something to server",sendMessage(s))
    s.close()
