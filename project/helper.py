import pickle
import os
import re
import socket
from pathlib import Path



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

    mess = 'send nodir "hola seniora\n sdaf \n"'
    # splitter = s.split()
    # print(splitter)
    # s = re.split('\"*\"', s)
    # print(s)
    # key = 0
    # for word in s:
    #     if key != 1:
    #         s[key] = word.replace(" ", "")
    #     # print(s.index(s[key]))
    #     key += 1
    # print(s)


    # Define the port on which you want to connect
    from project.messenger import Messenger

    cls = Messenger
    # cls.recieve_message()
    # connect to the server on local computer
    # users_data[receiver]["addr"][0]
    s = socket.socket()
    s.connect(("127.0.1.1", 2022))
    from project.protocol import Protocol
    resp = s.sendall("hola".encode())
    # resp = cls.send_socket_message(mess, Protocol.commands["send"], s)
    print(s.recv(1024))
    s.close()


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
    print(s)
    return s


def format_send_message(command):
    s = command
    receiver = command.split()[1]
    s = re.split('"', s)
    key = 0
    for word in s:
        if key != 1:
            s[key] = word.replace(" ", "")
        key += 1
    # print(s)
    return dict({
        "receiver": receiver,
        "message": s[1]
    })
