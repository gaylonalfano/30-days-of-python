# import os
import typing as t
import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from templates import Template

username: str = settings.USERNAME
password: str = settings.PASSWORD


class Emailer:
    def __init__(
        self,
        subject: str = "",
        from_email: str = "SMD <supermilkdaddy@gmail.com>",
        to_emails: t.List[str] = [],
        template_text_name: t.Optional[str] = None,
        context: t.Dict[str, str] = {},
        template_html_name: t.Optional[str] = None,
        has_html: bool = False,
    ):
        # Make sure at least one template has been passed
        if template_text_name is None and template_html_name is None:
            raise Exception("You must set a template.")

        assert isinstance(to_emails, list)

        self.subject = subject
        self.from_email = from_email
        self.to_emails = to_emails
        self.has_html = has_html
        self.template_text_name = template_text_name
        self.template_html_name = template_html_name
        self.context = context

        # Check that html template has been passed
        if template_html_name is not None:
            self.has_html = True

    def format_msg(self):
        # Construct email message with MIME
        msg = MIMEMultipart("alternative")
        msg["From"] = self.from_email
        msg["To"] = ", ".join(self.to_emails)
        msg["Subject"] = self.subject

        # If a text-type template was passed get the context
        if self.template_text_name is not None:
            template_filepath = Template(
                template_name=self.template_text_name, context=self.context
            )

            # context is already passed to template_filepath just need to render.
            template_content_string: str = template_filepath.render()
            txt_part = MIMEText(template_content_string, "plain")
            print(f"txt_part: {txt_part}")
            msg.attach(txt_part)

        if self.template_html_name is not None:
            template_filepath = Template(
                template_name=self.template_html_name, context=self.context
            )

            template_content_string: str = template_filepath.render()
            html_part = MIMEText(template_content_string, "html")
            print(f"html_part: {html_part}")
            msg.attach(html_part)

        msg_str: str = msg.as_string()

        return msg_str

    def send_mail(self):
        assert username is not None
        assert password is not None

        # Log into Gmail via smtp server. Create smtp server with smtplib
        did_send: bool = False
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as server:
            server.ehlo()
            server.starttls()
            server.login(user=username, password=password)
            try:
                server.sendmail(
                    from_addr=self.from_email,
                    to_addrs=self.to_emails,
                    msg=self.format_msg(),
                )
                did_send = True
            except:
                did_send = False

        return f"Email sent? {did_send}"


# print(os.getcwd())
# send_mail()


"""
NOTES:
    You can't just formulate an email. There are a lot of
    things that are required so you have to import other
    tools such as: MIMEText and MIMEMultipart (for HTML emails or files).
    Then you need to use these to construct your actual message.
"""
