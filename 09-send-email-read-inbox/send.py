import sys
import requests
from datetime import datetime

from formatting import format_msg
from send_mail import send_mail


def send(
    name: str, website: str = None, to_email: str = None, verbose: bool = False
):
    """
    Send formatted message.
    """
    assert to_email is not None

    if website is not None:
        msg = format_msg(name=name, website=website)
    else:
        msg = format_msg(name=name)

    if verbose:
        print(name, website, to_email)

    # Try sending the message
    try:
        send_mail(text=msg, to_emails=[to_email], html=None)
        sent = True
    except:
        sent = False
    return f"Message sent? {sent}"


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

    website = None
    if len(sys.argv) > 2:
        website = sys.argv[2]

    email = None
    if len(sys.argv) > 3:
        email = sys.argv[3]

    response = send(name=name, website=website, to_email=email, verbose=True)
    print(response)
