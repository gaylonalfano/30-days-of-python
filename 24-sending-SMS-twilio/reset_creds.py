import typing as t
from getpass import getpass


def reset_credentials(reset_creds: bool = True):
    """
    This will save our creds from above (blank or not) to a local .env file
    named so we can re-use these credentials.

    It's recommended to create new API keys for each new project so we
    can turn them off at anytime without causing disruption to other
    projects.
    """
    if reset_creds:
        twilio_sid: str = getpass("What's the Twilio Account SID?\n")
        twilio_secret: str = getpass("What's the Twilio Secret?\n")
        send_to_number: str = getpass("What's the number to send to?\n")
        send_from_number: str = getpass("What's the number to send from?\n")
        creds: t.Dict[str, str] = {
            "TWILIO_SID": twilio_sid,
            "TWILIO_SECRET": twilio_secret,
            "SEND_TO_NUMBER": f"+{send_to_number}",
            "SEND_FROM_NUMBER": f"+{send_from_number}",
        }
        # print(f"creds dict: {creds.items()}")

        # Create a concatenated string for each credential k:v pair
        # creds_lines: t.List[str] = []
        # for k, v in data.items():
        #     # Have to add newline for f.writelines()
        #     cred_line: str = f"{k}={v}\n"
        #     creds_lines.append(cred_line)
        creds_lines: t.List[str] = [f"{k}={v}\n" for k, v in creds.items()]

        # Now write each credential line to the .env file
        with open(".env", "w") as f:
            # Just write one line at a time:
            f.writelines(creds_lines)


# Let's try it:
reset_credentials(reset_creds=True)


# # TUTORIAL version using creds.json instead of .env
# import json
# from getpass import getpass

# reset_creds = False

# if reset_creds:
#     twilio_sid = getpass("What's the Twilio Account SID?")
#     twilio_secret = getpass("What's the Twilio Secret?")
#     '''
#     This will save our creds from above (blank or not) to a local file
#     named `creds.json` so we can re-use this credentials.
#     '''
#     data = {
#         "twilio_sid": twilio_sid,
#         "twilio_secret": twilio_secret
#     }
#     json_data = json.dumps(data)
#     with open('creds.json', 'w') as f:
#         f.write(json_data)
#
#
# Then load the credentials using
# TWILIO_SID: str
# TWILIO_SECRET: str
# with open("creds.json", "r") as f:
#     raw_data: str = f.read()
#     cred_data: t.Dict[str, str] = json.loads(raw_data)
#     TWILIO_SID = cred_data.get("twilio_sid")
#     TWILIO_SECRET = cred_data.get("twilio_secret")
