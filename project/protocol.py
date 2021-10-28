import base64
import json
import os
import sys
import re


class Protocol:
    message_encoding = "utf-8"
    ident_in_message = 3
    # protocol name : construction of protocol
    commands = {
        "MESSAGE": "MESSAGE",
        "AUTH": "AUTH",
        "FILE": "FILE"
    }

    @classmethod
    def encode_file(cls, file_path):
        #  first check file exist or not
        file = open(file_path, "r")
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1]
        size = os.path.getsize(file_path)
        print(file_name)
        print(file_ext)
        print(str(size) + " bytes")
        sys.exit()
        #  check there does file opened
        encoded = base64.b64encode(file.read())
        return json.JSONEncoder({
            "message": "encoded" + file_path,
            "file": {
                "ext": file_ext,
                "data": encoded
            }
        })

    @classmethod
    def decode_file(cls, json_data):
        data = json.JSONDecoder(json_data)
        print("file stored in /{username}/name")
        return "OK"

    @classmethod
    def defineCommand(cls, text):
        if len(text) < 0 and text == " ":
            return False
        wordList = re.sub("[^\w]", " ", text).split()
        if wordList[0] in cls.commands:
            return cls.commands[wordList[0]]

        return cls.commands["MESSAGE"]
