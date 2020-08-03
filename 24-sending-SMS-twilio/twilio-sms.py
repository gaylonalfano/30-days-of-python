# https://www.twilio.com/docs/sms/quickstart/python
import json
import typing as t
from twilio.rest import Client
import settings

"""
NOTES:
    - Can use Webhooks to handle actions when a message arrives.
      This could then send back a response or whatever.
    - To list out messages without using a Webhook.
    - Every message has an SID attached to each message instance
      created by Client(). You can use the SID to fetch the original
      message and details (body, date_sent, from_,etc.).
    - Use client.messages.list(limit=, to=, from_=) to retrieve a list
      of recent messages. Can see who is sending messages to your
      number (from_), etc.
    - CHALLENGE: Create a Webhook service to actually parse our messages
      data.


Example print of some of the message outputs:

SM3327e379a9374a2ca19356dbd36d1206
msg_ctx: <Twilio.Api.V2010.MessageContext account_sid=AC369f7149faf92c376e3d06a66f611118 sid=SM3327e379
a9374a2ca19356dbd36d1206>
msg_instance: <Twilio.Api.V2010.MessageInstance account_sid=AC369f7149faf92c376e3d06a66f611118 sid=SM33
27e379a9374a2ca19356dbd36d1206>
+19714075478
0: Sent from your Twilio trial account - Hello (again x 3) world SMS from Twilio
1: Sent from your Twilio trial account - Hello (again x 2) world SMS from Twilio
2: Sent from your Twilio trial account - Hello (again) world SMS from Twilio
3: Sent from your Twilio trial account - Hello world SMS from Twilio
"""

# Load Twilio credentials from creds.json
# TWILIO_SID: str
# TWILIO_SECRET: str
# with open("creds.json", "r") as f:
#     raw_data: str = f.read()
#     cred_data: t.Dict[str, str] = json.loads(raw_data)
#     TWILIO_SID = cred_data.get("twilio_sid")
#     TWILIO_SECRET = cred_data.get("twilio_secret")

# === Load Twilio credentials from settings.py
# http://twil.io/secure
twilio_sid: str = settings.TWILIO_SID
twilio_secret: str = settings.TWILIO_SECRET
send_to_number: str = settings.SEND_TO_NUMBER
send_from_number: str = settings.SEND_FROM_NUMBER

# === Create a Twilio Client
client = Client(twilio_sid, twilio_secret)

# === Send a message w/ our client
message = client.messages.create(
    body="Hello (again x 5) world SMS from Twilio",
    from_=send_from_number,
    to=send_to_number,
)

# === Handle messages (e.g, list recents msgs) w/o Webhooks
numbers_to_ignore: t.List[str] = []
# Let's store these inside ignore.json file
with open("numbers_to_ignore.json", "r") as f:
    data = json.loads(f.read())
    numbers_to_ignore = data.get("ignore")

# Each message instance (created by Client()) has an SID
# Can use the SID to fetch message details
msg_sid: str = message.sid
print(msg_sid)

msg_ctx = client.messages.get(msg_sid)
msg_instance = msg_ctx.fetch()
print(f"msg_ctx: {msg_ctx}")
print(f"msg_instance: {msg_instance}")
# List options available in the message instance:
# dir(msg_instance)
print(msg_instance.from_)  # or, .body, .to, etc.

# Iterate through recent messages
messages: t.List = client.messages.list(limit=20)  # from_=, to=
for i, msg in enumerate(messages):
    # Say we want to make hidden if in the ignore list
    from_: str = msg.from_
    to: str = msg.to
    if from_ in numbers_to_ignore:
        from_ = "~hidden~"
    if to in numbers_to_ignore:
        to = "~hidden~"
    # Messages sent from me?
    from_me: bool = False
    if from_ == send_to_number:
        from_me = True
    print(i, msg.body, to, from_, from_me)
    # print(f"{i}: {msg.body}", to, from_)
