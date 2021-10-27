import pickle

import jsonpickle
import json

from project.protocol import Protocol

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
        else:
            payload = dict({"message": data})
    else:
        payload = data
    return payload


def message_decoder(data):
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
        # print(msg)
        for key in msg:
            if key == "data":
                # print(type(msg["data"]))
                data = (message_decoder(msg["data"]))
                msg["data"] = data
        # print(msg)
        return msg


def test_functdd():
    data = "azamkhon"
    payload = format_payload(data)
    print(payload)
