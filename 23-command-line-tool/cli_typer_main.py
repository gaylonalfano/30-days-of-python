import typer

import cli_typer_items
import cli_typer_users

app = typer.Typer()
app.add_typer(cli_typer_users.app, name="users")
app.add_typer(cli_typer_items.app, name="items")

if __name__ == "__main__":
    app()
