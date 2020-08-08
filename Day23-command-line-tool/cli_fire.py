# # Easier approach using Google's fire package
# # BASIC
# import fire


# def hello(name: str = "World"):
#     return f"Hello, {name}"


# # # Next, to trigger fire we do:
# # if __name__ == "__main__":
# #     # We pass our function to the Fire() class
# #     # Can run 'python % --name Gaylon'
# #     fire.Fire(hello)


# # WITH INPUTS
# import typing as t
# from getpass import getpass
# import fire


# def login(name: t.Optional[str] = None):
#     # If --name isn't passed in command line:
#     if name is None:
#         # Prompt user:
#         name = input("What's your name?\n")
#     pw: str = getpass("What's your password?\n")
#     return name, pw  # ["Gaylon", "something"]


# # Next, to trigger fire we do:
# if __name__ == "__main__":
#     # We pass our function to the Fire() class
#     # Can run 'python % --name Gaylon'
#     fire.Fire(login)


# ADVANCED WITH SCRAPING PIPELINE (Day 22 StackOverflow)
"""
NOTES:
    - By Pipeline we can call multiple functions and classes.
    - Can pass just 'scrape' to call scrape_tag() function,
      which just returns a list of URLs.
    - Can even pass args along with 'scrape' command.
      E.g., python % scrape --tag "javascript"
    - Can create an entirely new class (e.g, Auth) that has
      a login() method. Then initialize that class INSIDE the
      Pipeline class by self.auth = Auth(). This will add another
      GROUP inside Fire called 'Auth', which has its own sub-commands.
    - Challenge: Could turn all the scrape SO functions into a class and
      then add/use that class within Pipeline class (self.my_class = MyClass())
      'python % auth login --username gaylon' -> ["gaylon", "mypassword"]
    - To read what the arguments are for any given function, you can use
      the signature() function inside the 'inspect' library and OrderedDict.


# Code from StackOverflow lesson:
def extract_data_from_url(url):
    r = requests.get(url)
    if r.status_code not in range(200, 299):
        return []
    html_str = r.text
    html = HTML(html=html_str)
    datas = parse_tagged_page(html)
    return datas


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

import typing as t
from getpass import getpass
import fire


# Can even create an entirely new class and add to Pipeline:
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


# Can even pass in other features like a login function:
def login(username: t.Optional[str] = None):
    if username is None:
        username = input("Username: ")
    if username is None:
        print("A username is required.")
        return
    pw: str = getpass("Password: ")
    return username, pw  # ["admin", "passecret"]


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
        # Just return a list of the URLs (for demo purpose only):
        # datas += extract_data_from_url(url)
        # time.sleep(1.5)
        datas.append(url)

    return datas


# Create Pipeline class
class Pipeline(object):
    # It's just an empty object with no arguments
    def __init__(self):
        # Set the various funcs we want to be associated with this class
        self.scrape = scrape_tag  # just func w/o args
        self.login = login
        self.auth = Auth()  # 'python % auth' will show sub-commands


# Next, to trigger fire we do:
if __name__ == "__main__":
    # Then just pass our Pipeline to the Fire() class
    # Now can pass 'scrape': python % scrape
    # Or even pass args to scrape: python % scrape --tag "javascript"
    # 'python % auth login --username gaylon' -> ["gaylon", "mypassword"]
    fire.Fire(Pipeline)
