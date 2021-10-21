env_vars = {
    "server_listening_port": 2021,
    "server_host": "localhost",
    "client_host": "localhost",
    "exit_word": "exit"
}


# all call backs should have at least 1 parameter socket data and should return response from connected device

def console_line(callback, user_data, input_message: str = "input something: ", use_input_m: bool = True,
                 exit_message: str = env_vars["exit_word"]):
    command = ''
    while command != exit_message:
        if use_input_m:
            command = callback(user_data, input_message)
            print("response: " + command)
        else:
            command = callback(user_data)

        if command == exit_message:
            user_data["socket"].close()
            break
