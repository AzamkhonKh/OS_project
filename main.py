import typer
from project.client import Client
from project.server import Server
from project.helper import *

app = typer.Typer()


@app.command()
def hello(name: str, iq: int):
    print(f"hello {name}")


@app.command()
def start_server():
    Server.start_server()


@app.command()
def start_client_test(username: str, ip="localhost"):
    Client.test(username, ip)


@app.command()
def test():
    test_functdd()


if __name__ == "__main__":
    app()
