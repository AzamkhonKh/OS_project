import typer
import client
from server import Server

app = typer.Typer()


@app.command()
def hello(name: str, iq: int):
    print(f"hello {name}")


@app.command()
def start_server(host: str = Server.host, port : int = int(Server.port)):
    Server.start_server(host, port)


@app.command()
def start_client_test(host: str = client.host, port: int = int(client.port)):
    client.test(host, port)


@app.command()
def goodbye(name: str, iq: int):
    print(f"goodbye {name}")


if __name__ == "__main__":
    app()
