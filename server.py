# first of all import the socket library
import socket
import _thread as thread
import sys

from helper import env_vars, console_line


class Server:
    port = env_vars['server_listening_port']
    host = env_vars['server_host']
    # it will be getted by ip in network or from env file (in future)

    users = dict()

    # username : dict(data like )
    @classmethod
    def start_server(cls):
        # next create a socket object
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket successfully created")

            s.bind((cls.host, cls.port))
            print("host is %s" % (cls.host))
            print("socket binded to %s" % (cls.port))

            s.listen(5)
            print("socket is listening")

            # a forever loop until we interrupt it or
            # an error occurs
            while True:
                # Establish connection with client.
                c, addr = s.accept()
                username = ''
                msg = c.recv(1024).decode()
                if msg.startswith("username: "):
                    username = msg[len("username: "):len(msg)]
                else:
                    print(f"received not username so closed connection ! recv({msg})")
                    c.close()
                print('Got connection from', username)
                cls.users[username] = {
                    "name": username,
                    "socket": s,
                    "addr": addr,
                    "connection": c,
                    "type": "server"
                }
                try:
                    thread.start_new_thread(cls.create_session, (c, cls.users[username]))
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
    def create_session(cls, c, user_data):
        c.send(f'Succes {user_data["name"]} ! \n'.encode())
        console_line(cls.receive_message_from_client, user_data, "", False)
        sys.exit()

    @classmethod
    def send_message_to_client(cls, msg, conn):
        conn.send(msg.encode())

    @classmethod
    def receive_message_from_client(cls, user_data):
        conn = user_data["connection"]
        message = conn.recv(1024).decode()
        print(f"received something from {user_data['name']}: " + message)
        if message != env_vars["exit_word"]:
            cls.send_message_to_client("recieved OK", conn)
        else:
            cls.send_message_to_client(message, conn)
        return message
