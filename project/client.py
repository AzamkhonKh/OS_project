import sys
import socket
from project.messenger import Messenger
from project.helper import *
from project.protocol import Protocol


# golsd
class Client:
    host = env_vars['client_host']
    port = env_vars['server_listening_port']
    msg = Messenger
    users_data_client = dict()

    @classmethod
    def sendMessageClient(cls, input_message: str = "input something: "):
        message = input(input_message)
        cmd = Protocol.defineCommand(message)
        if not cmd:
            pass
        else:
            return cls.send_socket_message(message, cmd)
            # return cls.receive_message(cmd)
        return cls.sendMessageClient("input something valid to send to server: ")

    @classmethod
    def test(cls, username: str):
        # Create a socket object
        s = socket.socket()

        # Define the port on which you want to connect

        # connect to the server on local computer
        s.connect((cls.host, cls.port))

        cls.users_data_client = {
            "name": username,
            "socket": s,
            "type": "client"
        }
        cls.send_socket_message(username, Protocol.commands["AUTH"])

        #  there serever should say smth like hey i see you clien
        #  if this not happens smth went wrong
        # print(cls.receive_message(Protocol.commands["AUTH"]))
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
        if command == Protocol.commands["LOCAL_LS"]:
            return cls.local_ls()
        elif command == Protocol.commands["write"] or command == Protocol.commands["overwrite"]:
            validation = cls.handle_sent_write(data)
            if validation == '':
                return "file does not exit in folder storage/client , please check before writing command by LOCAL_LS"
            else:
                data = Protocol.encode_file(validation)
        elif command == Protocol.commands["read"]:
            if cls.handle_sent_write(data) != '':
                return "file already exist in folder storage/client. use override function to update from server,  or delete it"
        elif command == Protocol.commands["appendfile"]:
            validation = cls.handle_sent_write(data)
            if validation == '':
                return "file does not exit in folder storage/client , please check before writing command by LOCAL_LS"

        payload = format_payload(data, command)
        payload = message_encoder(payload, command, 2)
        msg = message_encoder(payload, command)
        # print("_____________client payload")
        # print(payload)
        # print("________________")
        # print(msg)
        # cls.users_data_client["socket"].sendall(bytes(data_string, encoding=Protocol.message_encoding))
        cls.users_data_client["socket"].sendall(msg)
        return cls.receive_message(command)

    @classmethod
    def receive_message(cls, command: str = Protocol.commands["MESSAGE"], userSocket=None):
        #  this should be Json with
        # msg = cls.users_data_client["socket"].recv(1024).decode(Protocol.message_encoding)
        if userSocket is None:
            userSocket = cls.users_data_client["socket"]
        msg = userSocket.recv(1024)
        # data_loaded = pickle.loads(msg.encode(Protocol.message_encoding))
        msg = message_decoder(msg)
        if "command" in msg:
            command = msg["command"]
        if command == Protocol.commands["MESSAGE"]:
            return msg['data']['message']
        elif command == Protocol.commands["read"]:
            return cls.handle_read(msg)
        elif command == Protocol.commands["overread"]:
            return cls.handle_overread(msg)
        else:
            if "data" in msg:
                return msg['data']
            else:
                print("++____ smth went wrong msg do not have data key")
                print(msg)
                print("____________________________")
                if "message" in msg:
                    return msg
                else:
                    return dict({"message": "smth went wrong"})

        # if msg != '':
        #     print("received before decode" + loads)
        #     print(loads)

    @classmethod
    def local_ls(cls):
        txtfiles = []
        path = path_to_storage() + "/client"
        for file in glob.glob(path + "/*.*"):
            txtfiles.append(file)
        index = 1
        result = ''
        if txtfiles == []:
            return "there is no files located in " + path
        for file in txtfiles:
            result += "___________" + '\n'
            result += "INDEX - " + str(index) + " - " + file
            result += "___________" + '\n'
            index += 1

        return result

    @classmethod
    def store_file(cls, full_path, data):
        return Protocol.store_file(full_path, data)

    @classmethod
    def handle_sent_write(cls, command):
        # get name of file form command
        cmd = command.split()
        try:
            file_index = int(cmd[1])
            index = 1
            path = path_to_storage() + "/client"
            for file in glob.glob(path + "/*.*"):
                if file_index == index:
                    path = file
                    break
                index += 1

        except ValueError:
            filename = cmd[1]
            path = path_to_storage() + "/client/" + filename

        if os.path.isfile(path):
            return path
        else:
            return ''

    @classmethod
    def handle_read(cls, response):
        print("+++++++++++++++ response")
        print(response)
        print(type(response))
        print("+++++++++++++++_______________")
        data = response['data']
        path = path_to_storage() + "/client/"
        full_path = path + "/" + data['file_name'] + data['ext']
        return cls.store_file(full_path, data)


    @classmethod
    def handle_overread(cls, response):
        data = response['data']
        path = path_to_storage() + "/client/"
        full_path = path + data['file_name'] + data['ext']
        if os.path.isfile(full_path):
            os.remove(full_path)
        return cls.store_file(full_path, data)
