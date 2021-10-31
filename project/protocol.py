from project.helper import *
import base64
import os
import re


class Protocol:
    env_vars = {
        "server_listening_port": 2024,
        "server_host": "localhost",
        "client_host": "localhost",
        "exit_word": "exit",
        "messenger_port": 2022,
        "HEADERSIZE": 10
    }
    message_encoding = "utf-8"
    ident_in_message = 3
    # protocol name : construction of protocol // in ideal case
    commands = {
        "MESSAGE": "MESSAGE",
        "AUTH": "AUTH",
        "LOCAL_LS": "LOCAL_LS",
        "FILE": "FILE",
        "lu": "lu",
        "lf": "lf",
        "read": "read",
        "overread": "overread",
        "write": "write",
        "overwrite": "overwrite",
        "append": "append",
        "appendfile": "appendfile",

        "send": "send",
    }

    @classmethod
    def encode_file(cls, file_path):
        #  first check file exist or not
        with open(file_path, 'rb') as f:
            contents = f.read()
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1]
        name_without_ext = os.path.splitext(file_name)[0]
        size = os.path.getsize(file_path)
        # print(file_name)
        # print(file_ext)
        # print(str(size) + " bytes")
        #  check there does file opened
        encoded = base64.b64encode(contents)
        to_encode = dict({
            "message": "encoded file ready to store in server",
            "action": "storeFile",
            "size": size,
            "file_name": name_without_ext,
            "ext": file_ext,
            "base64_encoded": encoded
        })
        # data = helper.message_encoder(to_encode, cls.commands["FILE"], 2)
        # result = helper.message_encoder(data, cls.commands["FILE"])
        return to_encode

    @classmethod
    def store_file(cls, full_path, data):
        if os.path.isdir(full_path):
            return "given directory. not file location with name"
        if os.path.isfile(full_path):
            return "file with this name already exist"

        with open(full_path, "wb") as fh:
            fh.write(base64.decodebytes(data['base64_encoded']))
        return "file should be created " + full_path

    @classmethod
    def defineCommand(cls, text):
        if len(text) < 0 and text == " ":
            return False
        wordList = re.sub("[^\w]", " ", text).split()
        if wordList[0] in cls.commands:
            return cls.commands[wordList[0]]

        return cls.commands["MESSAGE"]

    # all call backs should have at least 1 parameter socket data and should return response from connected device

    @classmethod
    def console_line(cls, callback, user_data, input_message: str = "input something: ", client: bool = True,
                     exit_message=None):
        if exit_message is None:
            exit_message = cls.env_vars["exit_word"]
        command = ''
        while command != exit_message:
            if client:
                command = callback(input_message)
                if "message" in command:
                    command = command["message"]
                print(f"response: {command}")
            else:
                command = callback(user_data)

            if command == exit_message:
                if client:
                    user_data["socket"].close()
                else:
                    user_data["connection"].close()
                break

    @classmethod
    def message_encoder(cls, payload, command, mode=1):
        if mode == 1:
            msg = {
                "command": command,
                "message": command,
                "data": {
                    payload
                }
            }
        elif mode == 2:
            msg = payload
        else:
            raise Exception("unknown mode for encoding")
        # print("__________sending message !")
        # print(msg)
        # print("__________")
        msg = pickle.dumps(msg)
        msg = bytes(f"{len(msg):<{cls.env_vars['HEADERSIZE']}}", Protocol.message_encoding) + msg
        return msg

    @classmethod
    def format_payload(cls, data, command=None):
        if command is None:
            command = cls.commands["MESSAGE"]
        if isinstance(data, str):
            if command == Protocol.commands["AUTH"]:
                payload = dict({"username": data})
            elif command == Protocol.commands["FILE"]:
                payload = dict({
                    "message": " this is an file payload",
                    "filename": "smth.as/asdas",
                    "action": "write",
                    "file_data": cls.message_encoder({
                        "size": 123,
                        "ext": "jpg",
                        "bytes": "adfdf"
                    }, '', 2)
                })
            elif command == Protocol.commands["lf"]:
                payload = dict({
                    "message": "return list of available files in server",
                    "action": command,
                })
            elif command == Protocol.commands["lu"]:
                payload = dict({
                    "message": "return list of users in server",
                    "action": command,
                })
            elif command == Protocol.commands["append"]:
                splitted = format_append_message(data)
                payload = dict({
                    "message": "return list of users in server",
                    "file_name": splitted[2],
                    "append": splitted[1],
                    "action": command,
                })
            elif command == Protocol.commands["appendfile"]:
                splitted = data.split()
                path = path_to_storage() + "/client/" + splitted[1]
                print(path)
                file = open(path, "r")
                file_data = file.read()
                file.close()

                payload = dict({
                    "message": "return list of users in server",
                    "file_name": splitted[2],
                    "append": file_data,
                    "action": command,
                })
            elif command == Protocol.commands["read"] or command == Protocol.commands["overread"]:
                payload = dict({
                    "file_name": data.split()[1],
                    "action": command,
                })
            else:
                payload = dict({"message": data})
        else:
            payload = data
        return payload

    @classmethod
    def message_decoder(cls, data, conn=None, mode=1):
        # print("___________data")
        # # print(data)
        # print(type(data))
        # print("___________")

        if mode == 2:
            msg = data
        else:
            if isinstance(data, set):
                msg = next(iter(data))
                # print(msg)
            # elif isinstance(data, bytes):
            #     msg = pickle.loads(data.encode(Protocol.message_encoding))

            elif data is None or len(data) < cls.env_vars["HEADERSIZE"]:
                return ''
            else:
                msg = data
        full_msg = b''
        # print(msg)
        # print("new msg len:", msg[:cls.env_vars["HEADERSIZE"]])
        msglen = int(msg[:cls.env_vars["HEADERSIZE"]])

        # print(f"full message length: {msglen}")

        full_msg += msg

        # print(len(full_msg))

        if len(full_msg) - cls.env_vars["HEADERSIZE"] == msglen:
            msg = pickle.loads(full_msg[cls.env_vars["HEADERSIZE"]:])
            # print("___________msg HEADERSIZE")
            # print(msg)
            # print(type(msg))
            # print("___________")
            if isinstance(msg, dict):
                for key, value in msg.items():
                    if (isinstance(value, set) or isinstance(value, bytes)) and key != "base64_encoded":
                        # print("___________")
                        # print(key + "decoding")
                        # print("___________")
                        data = (cls.message_decoder(value))
                        msg[key] = data
                    # if key == "data":
                    #     # print(type(msg["data"]))
                    #     data = (message_decoder(msg["data"]))
                    #     msg["data"] = data
            return msg
        else:
            full_msg += conn.recv(1024)
            return cls.message_decoder(full_msg, conn, 2)

    @classmethod
    def path_to_storage(cls):
        return os.getcwd() + '/storage'