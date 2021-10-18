# first of all import the socket library
import socket
import _thread as thread
from helper import env_vars,console_line

class Server:
    port = env_vars['server_listening_port']
    host = env_vars['server_host']
    # it will be getted by ip in network or from env file (in future)

    users = []

    @classmethod
    def start_server(self,host, port):
        # next create a socket object
        s = socket.socket()
        print("Socket successfully created")

        s.bind((host, port))
        print("host is %s" % (host))
        print("socket binded to %s" % (port))

        s.listen(5)
        print("socket is listening")

        # a forever loop until we interrupt it or
        # an error occurs
        while True:
            # Establish connection with client.
            c, addr = s.accept()
            print('Got connection from', addr)
            try:
                thread.start_new_thread(self.create_session,(c, addr))
            except Exception as e:
                print('Error occured client closed message : ' + str(e))
                c.close()
            finally:
                print('out from try catch successfully !')
            # Close the connection with the client

    @classmethod
    def create_session(self, c, addr):
        print(addr)
        c.send('Succes azamkhon'.encode())
        # console_line()
        # raise Exception('error')
        c.close()
