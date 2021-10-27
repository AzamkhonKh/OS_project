import socket
import _thread as thread
import sys
import signal
from project.helper import *
from project.protocol import Protocol


class Server:
    s = None
    port = env_vars['server_listening_port']
    host = env_vars['server_host']
    # it will be getted by ip in network or from env file (in future)
    users = dict()

    # username : dict(data like )
    @classmethod
    def create_socket(cls):

        cls.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")

        cls.s.bind((cls.host, cls.port))
        print("host is %s" % cls.host)
        print("socket binded to %s" % cls.port)

        cls.s.listen(5)
        print("socket is listening")
        return cls.s

    @classmethod
    def start_server(cls):
        # next create a socket object
        signal.signal(signal.SIGINT, cls.ctrl_handler)
        s = cls.create_socket()
        try:
            # a forever loop until we interrupt it or
            # an error occurs
            while True:
                # Establish connection with client.
                c, addr = s.accept()
                cls.users["temp"] = {
                    "socket": s,
                    "addr": addr,
                    "connection": c,
                    "type": "server"
                }
                response = cls.receive_message_from_client(cls.users["temp"])
                if "username" in response.keys():
                    username = response["username"]
                else:
                    c.send(f'not found useraname so bye ! \n'.encode())
                    c.close()
                    continue
                if bool(cls.users) and (username in cls.users.keys()):
                    c.send(f'already have that user closing the connection username {username} ! \n'.encode())
                    c.close()
                    continue
                print('Got connection from', username)
                cls.users[username] = {
                    "name": username,
                    "socket": s,
                    "addr": addr,
                    "connection": c,
                    "type": "server"
                }
                # print(cls.users[username])
                try:
                    thread.start_new_thread(cls.create_session, (c, cls.users[username]))
                except Exception as e:
                    print('Error occured client closed message : ' + str(e))
                    c.close()
                    cls.start_server()
                    sys.exit()
                finally:
                    print('out from try catch successfully !')
                # Close the connection with the client
        except Exception as e:
            print('Error occured : ' + str(e))
            s.close()
            sys.exit()

    @classmethod
    def create_session(cls, c, user_data):

        try:
            cls.send_message_to_client(f'Succes {user_data["name"]} ! \n',c)
            console_line(cls.receive_message_from_client, user_data, "", False)
            if user_data["name"] in cls.users:
                del cls.users[user_data["name"]]
        except Exception as e:
            print('Error occured client closed message : ' + str(e))
            c.close()
            sys.exit()
        finally:
            print('out from try catch successfully !')

        # pop_result = cls.users.pop(user_data["name"],None)
        # if pop_result == user_data["name"]:
        #     print("successfullly deleted !")
        # elif pop_result == None:
        #     print("gived none")
        #     print(cls.users)
        # else:
        #     print(cls.users)

        c.close()
        sys.exit()

    @classmethod
    def send_message_to_client(cls, data, conn, command: str = Protocol.commands["MESSAGE"]):
        payload = format_payload(data)
        print("This is payload")
        print(payload)
        print("______________")
        message = message_encoder(payload, command, 2)
        msg = message_encoder(message, command)
        conn.sendall(msg)

    @classmethod
    def receive_message_from_client(cls, user_data):
        conn = user_data["connection"]
        msg = conn.recv(1024)
        # data_loaded = pickle.loads(msg.encode(Protocol.message_encoding))
        msg = message_decoder(msg)
        if msg["message"] == "MESSAGE":
            message = msg["data"]["message"]
        elif msg["message"] == "AUTH":
            message = msg["data"]
        else:
            message = msg['data']['message']

        print("received mesage: ")
        print(message)
        print("_________________")
        if "name" in user_data:
            print(f"received something from {user_data['name']}: " + msg)
        if message != env_vars["exit_word"]:
            cls.send_message_to_client("recieved OK", conn)
        else:
            cls.send_message_to_client(message, conn)
        return message

    @classmethod
    def ctrl_handler(cls, signum, frame):
        print("in handler")
        for user in cls.users.keys():
            cls.users[user]["connection"].close()
        cls.s.close()
        sys.exit()

