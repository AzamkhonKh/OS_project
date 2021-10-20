# first of all import the socket library
import socket
import _thread as thread
import sys
from time import sleep

from helper import env_vars, console_line


class Server:
    port = env_vars['server_listening_port']
    host = env_vars['server_host']
    # it will be getted by ip in network or from env file (in future)

    users = []

    @classmethod
    def start_server(cls, host, port):
        # next create a socket object
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
                    thread.start_new_thread(cls.create_session, (c, addr))
                except Exception as e:
                    print('Error occured client closed message : ' + str(e))
                    sys.exit()
                finally:
                    print('out from try catch successfully !')
                # Close the connection with the client
        except Exception as e:
            print('Error occured : ' + str(e))
            sys.exit()

    @classmethod
    def create_session(self, c, addr):
        print(addr)
        c.send('Succes azamkhon ! \n'.encode())
        # console_line()
        # raise Exception('error')
        message = ''
        while True:
            message = c.recv(1024).decode()
            if message != env_vars["exit_word"]:
                print("received something: " + message)
                self.send_message_to_client("recieved OK", c)
                sleep(5)
            else:
                break
        c.send(env_vars["exit_word"].encode())
        c.close()
        sys.exit()

    @classmethod
    def send_message_to_client(cls, msg, conn):
        conn.send(msg.encode())
