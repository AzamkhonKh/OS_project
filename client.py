# Import socket module
import socket
from helper import env_vars

host = env_vars['client_host']
port = env_vars['server_listening_port']


def test(host, port):
        # Create a socket object
        s = socket.socket()

        # Define the port on which you want to connect

        # connect to the server on local computer
        s.connect((host, port))

        # receive data from the server and decoding to get the string.
        print(s.recv(1024).decode())
        # close the connection
        s.close()