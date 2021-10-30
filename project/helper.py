import pickle
from project.protocol import Protocol
import os
import glob
import re
import base64
from pathlib import Path

env_vars = {
    "server_listening_port": 2021,
    "server_host": "localhost",
    "client_host": "localhost",
    "exit_word": "exit",
    "messenger_port": 2022,
    "HEADERSIZE": 10
}


# all call backs should have at least 1 parameter socket data and should return response from connected device

def console_line(callback, user_data, input_message: str = "input something: ", client: bool = True,
                 exit_message: str = env_vars["exit_word"]):
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


def message_encoder(payload, command, mode=1):
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
    msg = bytes(f"{len(msg):<{env_vars['HEADERSIZE']}}", Protocol.message_encoding) + msg
    return msg


def format_payload(data, command=Protocol.commands["MESSAGE"]):
    if isinstance(data, str):
        if command == Protocol.commands["AUTH"]:
            payload = dict({"username": data})
        elif command == Protocol.commands["FILE"]:
            payload = dict({
                "message": " this is an file payload",
                "filename": "smth.as/asdas",
                "action": "write",
                "file_data": message_encoder({
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


def message_decoder(data, conn=None, mode=1):
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

        elif data is None or len(data) < env_vars["HEADERSIZE"]:
            return ''
        else:
            msg = data
    full_msg = b''
    # print(msg)
    # print("new msg len:", msg[:env_vars["HEADERSIZE"]])
    msglen = int(msg[:env_vars["HEADERSIZE"]])

    # print(f"full message length: {msglen}")

    full_msg += msg

    # print(len(full_msg))

    if len(full_msg) - env_vars["HEADERSIZE"] == msglen:
        msg = pickle.loads(full_msg[env_vars["HEADERSIZE"]:])
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
                    data = (message_decoder(value))
                    msg[key] = data
                # if key == "data":
                #     # print(type(msg["data"]))
                #     data = (message_decoder(msg["data"]))
                #     msg["data"] = data
        return msg
    else:
        full_msg += conn.recv(1024)
        return message_decoder(full_msg, conn, 2)


def test_functdd():
    # my_dict = {'message': 'FILE',
    #            'data': {'message': ' this is an file payload', 'filename': 'smth.as/asdas', 'action': 'write',
    #                     'file_data': b'53        \x80\x04\x95*\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x04size\x94K{\x8c\x03ext\x94\x8c\x03jpg\x94\x8c\x05bytes\x94\x8c\x05adfdf\x94u.'}}
    # print(type(my_dict['data']['file_data']))
    # for key, val in my_dict.items():
    #     if isinstance(val, dict):
    #         for key1, val1 in val.items():
    #             if isinstance(val1, bytes):
    #                 data = message_decoder(val1)
    #                 val[key1] = data
    #     elif isinstance(val, set):
    #         data = (message_decoder(val))
    #         my_dict[key] = data
    #     print(val)
    #     print(type(val))
    # print(my_dict)
    # protocol = Protocol()
    # txtfiles = []
    # for file in glob.glob(path_to_storage() + "/client/*.*"):
    #     txtfiles.append(file)
    # print(txtfiles)
    # encoded_file = protocol.encode_file(txtfiles[0])
    # # print(encoded_file)
    # decoded_file = message_decoder(encoded_file)
    # print(decoded_file)
    # data = decoded_file['data']
    # store_path = path_to_storage() + "/server/jumobot/"
    # Path(store_path).mkdir(parents=True, exist_ok=True)
    # with open(store_path + data['file_name'] + data['ext'], "wb") as fh:
    #     fh.write(base64.decodebytes(data['base64_encoded']))

    s = 'append "\n seniorita asdf as fs" hola.txt'

    s = re.split('"', s)
    print(s)
    key = 0
    for word in s:
        if key != 1:
            s[key] = word.replace(" ", "")
        print(s.index(s[key]))
        key += 1
    print(s)


def path_to_storage():
    return os.getcwd() + '/storage'


def format_append_message(command):
    s = command
    s = re.split('"', s)
    key = 0
    for word in s:
        if key != 1:
            s[key] = word.replace(" ", "")
        key += 1
    # print(s)
    return s
