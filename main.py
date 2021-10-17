import typer

app = typer.Typer()

@app.command()
def hello(name: str, iq: int):
    print(f"hello {name}")

@app.command()
def goodbye(name: str, iq: int):
    print(f"goodbye {name}")

app()
