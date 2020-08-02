# FastAPI's CLI sibling
import typer


def main(name: str):
    typer.echo(f"Hello {name}")
