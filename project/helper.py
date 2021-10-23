import jsonpickle
import json

env_vars = {
    "server_listening_port": 2021,
    "server_host": "localhost",
    "client_host": "localhost",
    "exit_word": "exit",
    "messenger_port": 2022
}


# all call backs should have at least 1 parameter socket data and should return response from connected device

def console_line(callback, user_data, input_message: str = "input something: ", client: bool = True,
                 exit_message: str = env_vars["exit_word"]):
    command = ''
    while command != exit_message:
        if client:
            command = callback(user_data, input_message)
            print("response: " + command)
        else:
            command = callback(user_data)

        if command == exit_message:
            if client:
                user_data["socket"].close()
            else:
                user_data["connection"].close()
            break


def test_functdd():
    data = "azamkhon"
    if data is str:
        payload = {"message": data}
    else:
        payload = data
    msg = {
        "message": "AUTH",
        "data": {
            payload
        }
    }
    print(msg)

    data_string = jsonpickle.encode(msg)

    print(data_string)
    decoded = jsonpickle.decode(data_string)
    print(decoded)


