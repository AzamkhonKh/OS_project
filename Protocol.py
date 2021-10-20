import base64
import json


class Protocol:
    @classmethod
    def encode_file(cls, file_path):
        file_ext = file_path
        #  check there does file opened
        data = open(file_path, "r").read()
        encoded = base64.b64encode(data)
        return json.JSONEncoder({
            "message": "encoded" + file_path,
            "file": {
                "ext": file_ext,
                "data": encoded
            }
        })

    @classmethod
    def decode_file(cls,json_data):
        data = json.JSONDecoder(json_data)
        print("file stored in /{username}/name")
        return "OK"
