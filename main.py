import typer
import client
from server import Server

app = typer.Typer()


@app.command()
def hello(name: str, iq: int):
    print(f"hello {name}")


@app.command()
def start_server(host: str = Server.host):
    Server.start_server()


@app.command()
def start_client_test(username: str, host: str = client.host, port: int = int(client.port)):
    client.test(username, host, port)


@app.command()
def goodbye(name: str, iq: int):
    print(f"goodbye {name}")


if __name__ == "__main__":
    app()
