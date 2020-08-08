# The hard way using sys.argv
import sys


if __name__ == "__main__":
    try:
        name: str = sys.argv[1]
    except
        name: str = input("What's your name?\n")

    from getpass import getpass
    pw: str = getpass("What's your password?\n")
    print(name, pw)
