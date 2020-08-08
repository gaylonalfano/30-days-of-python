import sys
import requests
from datetime import datetime

from formatting import format_msg


def send(name: str, website: str = None, verbose: bool = False):
    """
    Send formatted message.
    """
    if website is not None:
        msg = format_msg(name=name, website=website)
    else:
        msg = format_msg(name=name)

    if verbose:
        print(name, website)
    # Send the message
    response = requests.get("http://httpbin.org/json")

    if response.status_code == 200:
        return response.json()
    else:
        return "There was an error!"


# Non-pythonic way of automatically running our function
# This way if we import this module it won't auto call.
# response = send("Justin", verbose=True)
# print(response)

# To run our function automatically when module is loaded
if __name__ == "__main__":
    print(sys.argv)  # command line args passed ['send.py', 'abc', 'yada']

    name = "Unknown"

    if len(sys.argv) > 1:
        name = sys.argv[1]

    response = send(name, verbose=True)
    print(response)
