import glob
import os
import socket
import _thread as thread
import sys
import signal

from project.protocol import Protocol
from project.messenger import *
from pathlib import Path


class Server:
    s = None
    port = Protocol.env_vars['server_listening_port']
    host = Protocol.env_vars['server_host']
    # it will be getted by ip in network or from env file (in future)
    users = dict()

    # username : dict(data like )
    @classmethod
    def create_socket(cls, with_print = True):

        cls.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if with_print:
            print("Socket successfully created")

        cls.s.bind((cls.host, cls.port))
        if with_print:
            print("host is %s" % cls.host)
            print("socket binded to %s" % cls.port)

        cls.s.listen(5)
        if with_print:
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
                if isinstance(response, bool):
                    c.close()
                    continue
                else:
                    new_user = cls.users[response["name"]] = response
                # print(cls.users[username])
                try:
                    thread.start_new_thread(cls.create_session, (c, new_user))
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
            Protocol.console_line(cls.receive_message_from_client, user_data, "", False)
            if user_data["name"] in cls.users:
                del cls.users[user_data["name"]]
        except Exception as e:
            print('Error occured client closed message : ' + str(e))
            c.close()
            sys.exit()

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
        payload = Protocol.format_payload(data, command)

        # print("This is payload")
        # print(payload)
        # print(command)
        # print("______________")
        message = Protocol.message_encoder(payload, command, 2)
        msg = Protocol.message_encoder(message, command)

        # print("This is msg")
        # print(msg)
        # print(command)
        # print("______________")
        conn.sendall(msg)

    @classmethod
    def receive_message_from_client(cls, user_data):
        conn = user_data["connection"]
        # msg = cls.recvallMine(conn)
        msg = conn.recv(1024)
        # data_loaded = pickle.loads(msg.encode(Protocol.message_encoding))
        msg = Protocol.message_decoder(msg, conn)
        if msg["command"] == Protocol.commands["MESSAGE"]:
            message = msg["data"]["message"]
        elif msg["command"] == Protocol.commands["AUTH"]:
            return cls.hanlde_auth(msg, user_data)
        elif msg["command"] == Protocol.commands["FILE"]:
            message = cls.handle_file(msg, user_data)
        elif msg["command"] == Protocol.commands["lf"]:
            return cls.handle_lf(user_data)
        elif msg["command"] == Protocol.commands["lu"]:
            return cls.handle_lu(user_data)
        elif msg["command"] == Protocol.commands["write"]:
            return cls.handle_write(msg, user_data)
        elif msg["command"] == Protocol.commands["overwrite"]:
            return cls.handle_overwrite(msg, user_data)
        elif msg["command"] == Protocol.commands["read"] or msg["command"] == Protocol.commands["overread"]:
            return cls.handle_read(msg, user_data)
        elif msg["command"] == Protocol.commands["append"]:
            return cls.handle_append(msg, user_data)
        elif msg["command"] == Protocol.commands["appendfile"]:
            return cls.handle_append(msg, user_data)
        elif msg["command"] == Protocol.commands["send"]:
            return cls.handle_send(msg, user_data)
        else:
            message = msg['data']['message']

        # print("received mesage: ")
        # print(message)
        # print("_________________")
        if "name" in user_data:
            print(f"received something from {user_data['name']}: " + message)
        if message != Protocol.env_vars["exit_word"]:
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

    @classmethod
    def hanlde_auth(cls, msg, user_data):
        conn = user_data["connection"]
        response = msg["data"]

        print("_____________ msg auth handle")
        print(msg)
        print("_____________++++++++++")
        conn = user_data["connection"]
        if "username" in response.keys():
            username = response["username"]
        else:
            cls.send_message_to_client(f'not found useraname so bye ! \n', conn)
            return False
        if bool(cls.users) and (username in cls.users.keys()):
            cls.send_message_to_client(
                f'already have that user closing the connection username {username} ! \n', conn)
            return False
        print('Got connection from', username)
        cls.send_message_to_client('Succes ' + username + ' ! \n', conn)
        return {
            "name": username,
            "socket": user_data["socket"],
            "addr": user_data["addr"],
            "connection": conn,
            "type": "server"
        }

    @classmethod
    def handle_file(cls, msg, user_data):
        decoded_file = msg
        # print(msg)
        dir_name = Protocol.path_to_storage() + "/server/" + user_data['name']
        Path(dir_name).mkdir(parents=True, exist_ok=True)
        message = "file should be crated " + dir_name
        # print(message)
        # Protocol.decode_file()
        print(decoded_file)
        data = decoded_file['data']
        full_path = dir_name + data['file_name'] + data['ext']
        if "action" in data:
            if data["action"] == "storeFile":
                cls.store_file(full_path, data)
            # if data["action"] == "open":
            #     cls.send_file(full_path, data)

        else:
            cls.store_file(full_path, data)
        return message

    @classmethod
    def handle_lf(cls, user_data):
        txtfiles = []
        result = ''
        index = 1
        conn = user_data["connection"]
        full_path = Protocol.path_to_storage() + "/server/" + user_data['name']
        Path(full_path).mkdir(parents=True, exist_ok=True)
        files_available = False
        for file in glob.glob(full_path + "/*.*"):
            files_available = True
            result += '\n'
            result += str(index) + " - " + os.path.basename(file)
            result += '\n'
            index += 1

        if not files_available:
            result = "folder is empty add some file viw write command " + full_path
        cls.send_message_to_client(result, conn)
        return result

    @classmethod
    def store_file(cls, full_path, data):
        if os.path.isdir(full_path):
            full_path += data['file_name'] + data['ext']

        return Protocol.store_file(full_path, data)

    @classmethod
    def handle_lu(cls, user_data):
        conn = user_data["connection"]
        result = ''
        index = 1
        for username in cls.users.keys():
            if username == "temp":
                continue
            result += str(index) + " - " + username + '\n'
            index += 1

        if result == '':
            result = "there is no user rather than you ! )"
        cls.send_message_to_client(result, conn)
        return result

    @classmethod
    def handle_write(cls, msg, user_data):
        decoded_file = msg
        conn = user_data["connection"]
        dir_name = Protocol.path_to_storage() + "/server/" + user_data['name']
        Path(dir_name).mkdir(parents=True, exist_ok=True)
        data = decoded_file['data']
        # print("________ data before store file")
        # print(data)
        # print("________@@@@@@@")
        full_path = dir_name + "/" + data['file_name'] + data['ext']
        message = cls.store_file(full_path, data)
        cls.send_message_to_client(message, conn)
        return message

    @classmethod
    def handle_overwrite(cls, msg, user_data):
        data = msg['data']
        dir_name = Protocol.path_to_storage() + "/server/" + user_data['name']
        full_path = dir_name + "/" + data['file_name'] + data['ext']
        if os.path.isfile(full_path):
            os.remove(full_path)
        cls.handle_write(msg, user_data)

    @classmethod
    def handle_read(cls, msg, user_data):
        # there are handling read and overread
        # get filen_name
        print("_____________ msg read handle")
        print(msg)
        print("_____________++++++++++")
        command = Protocol.commands["MESSAGE"]
        conn = user_data["connection"]
        file_name = msg['data']['file_name']
        # check does file exist
        dir_name = Protocol.path_to_storage() + "/server/" + user_data['name']
        full_path = dir_name + "/" + file_name
        if os.path.isfile(full_path):
            # if msg['command'] == Protocol.commands["overread"]:
            command = msg['command']
            message = Protocol.encode_file(full_path)
        else:
            message = "file not found in server " + full_path
        cls.send_message_to_client(message, conn, command)
        return message

    @classmethod
    def handle_append(cls, msg, user_data):
        conn = user_data["connection"]
        file_name = msg['data']['file_name']
        dir_name = Protocol.path_to_storage() + "/server/" + user_data['name']
        full_path = dir_name + "/" + file_name
        # print(full_path)
        if os.path.isfile(full_path):
            append_string = msg['data']['append']
            file_object = open(full_path, 'a')
            file_object.write(append_string)
            file_object.close()
            message = "success ! appended string to file"
        else:
            message = "file not exist, pls use lf to check spelling ( " + full_path + " )"
        cls.send_message_to_client(message, conn)
        return message

    @classmethod
    def handle_send(cls, msg, user_data):

        # print("_____________ msg send handle")
        # print(msg)
        # print("_____________++++++++++")
        conn = user_data["connection"]
        data = msg['data']
        receiver = data['receiver']
        message = data['message']
        from project.messenger import Messenger
        result = Messenger.send_message(user_data["name"], receiver, cls.users, message)
        cls.send_message_to_client(result, conn)
        return result
