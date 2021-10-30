import base64
import project.helper as helper
import json
import os
import re


class Protocol:
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
