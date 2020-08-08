import imaplib
import email
import typing as t
import settings

host = "imap.gmail.com"

username: str = settings.USERNAME
password: str = settings.PASSWORD

# Log into mail server and select main "inbox"
mail = imaplib.IMAP4_SSL(host=host)
mail.login(user=username, password=password)
mail.select(mailbox="INBOX")

# Specify which emails to retrieve. Using 'SEEN' for constant list.
_, search_data = mail.search(None, "UNSEEN")
# _, search_data = mail.search(None, "SEEN")
# print(search_data)  # [b'2 3 4 5']

# Create empty list to store messages (dict)
my_messages: t.List[dict] = []


def get_inbox() -> t.List[dict]:
    """
    Loop through specified mail search data and store
    message components in a list of dict object.
    """
    for message_num in search_data[0].split():  # [b'2', b'3', b'4', b'5']
        # Create a dict to store the part of the message
        email_data = {}
        # Interact with actual email message using mail.fetch()
        _, data = mail.fetch(message_num, "(RFC822)")
        # print(type(data))  # list of tuples
        # print(data[0])  # tuple
        part_a, part_b = data[0]
        # print(part_b)  # Crazy long BYTE str:
        """
           b'Return-Path: <supermilkdaddy@gmail.com>\r\nReceived: from 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.
           0.0.0.0.0.0.ip6.arpa ([107.172.97.122])\r\n        by smtp.gmail.com with ESMTPSA id n18sm6148491pfd.99.2020.07.
           16.19.07.41\r\n        for <supermilkdaddy@gmail.com>\r\n        (version=TLS1_3 cipher=TLS_AES_256_GCM_SHA384 b
           its=256/256);\r\n        Thu, 16 Jul 2020 19:07:43 -0700 (PDT)\r\nMessage-ID: <5f1107ef.1c69fb81.287fa.2dbe@mx.g
           oogle.com>\r\nDate: Thu, 16 Jul 2020 19:07:43 -0700 (PDT)\r\nContent-Type: multipart/alternative; boundary="====
           ===========5198110372007756581=="\r\nMIME-Version: 1.0\r\nFrom: SMD <supermilkdaddy@gmail.com>\r\nTo: supermilkd
           addy@gmail.com\r\nSubject: Email subject\r\n\r\n--===============5198110372007756581==\r\nContent-Type: text/pla
           in; charset="us-ascii"\r\nMIME-Version: 1.0\r\nContent-Transfer-Encoding: 7bit\r\n\r\n\r\nHello Gaylon,\r\nThank
            you for joining cfe.sh. We are very happy to have you with us.\r\n\r\n--===============5198110372007756581==--\
           r\n'
        """
        email_message: t.Dict[str, str] = email.message_from_bytes(part_b)
        # print(type(email_message))  # <class 'email.message.Message'>
        for header in ["subject", "to", "from", "date"]:
            # print(f"{header}: {email_message[header]}")
            email_data[header] = email_message[header]

        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                # Convert bytes b' to normal STR type using decode()
                # print(body.decode())
                email_data["body"] = body.decode()
            elif part.get_content_type() == "text/html":
                html_body = part.get_payload(decode=True)
                # print(html_body.decode())
                email_data["html_body"] = html_body.decode()

        # Append email_data dict obj to my_messages list
        my_messages.append(email_data)

    return my_messages


if __name__ == "__main__":
    my_inbox = get_inbox()
    print(my_inbox)


"""
    NOTES:
    - Login to mail server and select the inbox
    - Specify which emails to retrieve using mail.search()
    - Loop through emails and fetch parts using mail.fetch()
    - Extract the part you need and store using email.message_from_bytes
    - Further parse the email message and extract the text/plain and text/html strings
    - Save the parts of the email message inside a email_data dict
    - Then store ALL email messages (dicts) inside a list my_messages
    - Finally wrap all the above inside a get_inbox() function that returns my_messages list
    - Then add the if __name__ == "__main__" to control what happens when module (inbox.py) is called
"""
