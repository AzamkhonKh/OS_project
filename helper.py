env_vars = {
    "server_listening_port": 2021,
    "server_host": "localhost",
    "client_host": "localhost",

}


def console_line(msg, callback):
    command = ''
    while command != "exit":
        command = input(msg)
        callback(command)
