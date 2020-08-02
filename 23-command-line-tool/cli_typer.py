# FastAPI's CLI sibling
# # BASIC
# import typer


# def main(name: str):
#     typer.echo(f"Hello {name}")


# if __name__ == "__main__":
#     typer.run(main)

"""
NOTES:
    - To run it: python % gaylon
    - Has a nice --help
    - Simply call app() to explicitly create a typer.Typer app.
    - The previous/basic typer.run actually creates one implicitly for you.
    - Add two subcommands with @app.command()
    - Execute the app() itself, as if it was a function (instead of typer.run)
    - Run it using 'python % goodbye Ashley --formal'
    - Typer adds command GROUPS similar to Fire, but you create them as separate
      typer.Typer() apps (e.g, in diff files items.py, users.py, main.py) and then
      bring together in main.py using app.add_typer(items.app, name="items").

If you don't pass any argument:
Usage: cli_typer.py [OPTIONS] NAME
Try 'cli_typer.py --help' for help.

Error: Missing argument 'NAME'.

def scrape_tag(
    tag: str = "python",
    query_filter: str = "Votes",
    max_pages: int = 50,
    pagesize: int = 25,
):
    base_url: str = "https://stackoverflow.com/questions/tagged/"
    datas: t.List = []
    for page in range(max_pages):
        page_num: int = page + 1
        url: str = f"{base_url}{tag}?tab={query_filter}&page={page_num}&pagesize={pagesize}"
        datas += extract_data_from_url(url)
        time.sleep(1.5)
    return datas
"""
# ADVANCED - Create a typer.Typer() app and two subcommands w/params
import typing as t
from getpass import getpass
import typer

app = typer.Typer()


class Auth(object):
    # Now our login() func is a class method
    def login(self, username: t.Optional[str] = None):
        if username is None:
            username = input("Username: ")
        if username is None:
            print("A username is required.")
            return
        pw: str = getpass("Password: ")
        return username, pw  # ["admin", "passecret"]


@app.command()
def login(username: t.Optional[str] = None):
    if username is None:
        username = input("Username: ")
    if username is None:
        print("A username is required.")
        return
    pw: str = getpass("Password: ")
    return username, pw  # ["admin", "passecret"]


@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        typer.echo(f"Goodbye Ms. {name}. Have a good day!")
    else:
        typer.echo(f"Bye {name}!")


# @app.command(name=login, cls=Auth())
# def scrape_tag(
#     tag: str = "python",
#     query_filter: str = "Votes",
#     max_pages: int = 50,
#     pagesize: int = 25,
# ):
#     base_url: str = "https://stackoverflow.com/questions/tagged/"
#     datas: t.List = []
#     for page in range(max_pages):
#         page_num: int = page + 1
#         url: str = f"{base_url}{tag}?tab={query_filter}&page={page_num}&pagesize={pagesize}"
#         datas += extract_data_from_url(url)
#         time.sleep(1.5)
#     return datas


if __name__ == "__main__":
    # Simply call app() to explicitly create a typer.Typer app.
    # The previous/basic typer.run actually creates one implicitly for you.
    # Add two subcommands with @app.command()
    # Execute the app() itself, as if it was a function (instead of typer.run)
    app()
