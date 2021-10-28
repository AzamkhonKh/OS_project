import pickle
from project.protocol import Protocol
import os
import glob
import re

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
            "message": command,
            "data": {
                payload
            }
        }
    elif mode == 2:
        msg = payload
    else:
        raise Exception("unknown mode for encoding")
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
        else:
            payload = dict({"message": data})
    else:
        payload = data
    return payload


def message_decoder(data):
    # print("___________data")
    # print(data)

    # print("___________")
    if isinstance(data, set):
        msg = next(iter(data))
        # print(msg)
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
        # print("___________msg")
        # print(msg)
        # print(type(msg))
        # print("___________")
        if isinstance(msg, dict):
            for key, value in msg.items():
                if isinstance(value, set) or isinstance(value, bytes):
                    # print("___________")
                    # print(key + "decoding")
                    # print("___________")
                    data = (message_decoder(value))
                    msg[key] = data
                # if key == "data":
                #     # print(type(msg["data"]))
                #     data = (message_decoder(msg["data"]))
                #     msg["data"] = data
        # print(msg)
        return msg


def test_functdd():
    my_dict = {'message': 'FILE',
               'data': {'message': ' this is an file payload', 'filename': 'smth.as/asdas', 'action': 'write',
                        'file_data': b'53        \x80\x04\x95*\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x04size\x94K{\x8c\x03ext\x94\x8c\x03jpg\x94\x8c\x05bytes\x94\x8c\x05adfdf\x94u.'}}
    print(type(my_dict['data']['file_data']))
    for key, val in my_dict.items():
        if isinstance(val, dict):
            for key1, val1 in val.items():
                if isinstance(val1,bytes):
                    data = message_decoder(val1)
                    val[key1] = data
        elif isinstance(val, set):
            data = (message_decoder(val))
            my_dict[key] = data
        print(val)
        print(type(val))
    print(my_dict)
    # mystr = 'This is a string, with words!'
    # wordList = re.sub("[^\w]", " ", mystr).split()
    # print(wordList[0])
    # dir_name = os.getcwd()
    # print(dir_name)
    #
    # txtfiles = []
    # for file in glob.glob(dir_name + "/*.*"):
    #     txtfiles.append(file)
    # print(txtfiles)
