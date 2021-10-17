import typer

import client
import server

app = typer.Typer()


@app.command()
def hello(name: str, iq: int):
    print(f"hello {name}")


@app.command()
def start_server(host: str = server.host, port=server.port):
    port = int(port)
    # print(type(host))
    # print(host + "  " + str(port))
    server.start_server('', port)


@app.command()
def start_client(host: str = client.host, port: int = int(client.port)):
    client.test('127.0.0.1', port)


@app.command()
def goodbye(name: str, iq: int):
    print(f"goodbye {name}")


if __name__ == "__main__":
    app()
