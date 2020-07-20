# import os
import typing as t
import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

username: str = settings.USERNAME
password: str = settings.PASSWORD


def send_mail(
    text: str = "Email body",
    subject: str = "Email subject",
    from_email: str = "SMD <supermilkdaddy@gmail.com>",
    to_emails: t.List[str] = [],
    html=None,
):

    assert isinstance(to_emails, list)
    assert username is not None
    assert password is not None

    # Construct email message with MIME
    msg = MIMEMultipart("alternative")
    msg["From"] = from_email
    msg["To"] = ", ".join(to_emails)
    msg["Subject"] = subject

    txt_part = MIMEText(text, "plain")
    msg.attach(txt_part)

    if html is not None:
        html_part = MIMEText("<h1>This is the HTML_part</h1>", "html")
        msg.attach(html_part)

    msg_str = msg.as_string()

    # Log into Gmail via smtp server. Create smtp server with smtplib
    # # Syntax 1: Without context manager
    # server = smtplib.SMTP()

    # server.quit()

    # Syntax 2: With context manager:
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as server:
        server.ehlo()
        server.starttls()
        server.login(user=username, password=password)
        server.sendmail(from_addr=from_email, to_addrs=to_emails, msg=msg_str)


# print(os.getcwd())
# send_mail()


"""
NOTES:
    You can't just formulate an email. There are a lot of
    things that are required so you have to import other
    tools such as: MIMEText and MIMEMultipart (for HTML emails or files).
    Then you need to use these to construct your actual message.
"""
