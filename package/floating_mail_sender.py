"""
The module is responsible for sending an email message to the addressee by attaching the finished report
"""

import json
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib


class Sender:
    """
    Contains a method for sending a message
    """

    def __init__(self, subject: str, filename: str):
        self.subject = subject
        self.filename = filename

    def send_mail(self):
        """
        Sends an email to the addressee
        """

        with open("config.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        login = data["login"]
        password = data["password"]
        receiver = data["receiver"]

        msg = MIMEMultipart()
        msg["From"] = login
        msg["To"] = receiver
        msg["Subject"] = self.subject

        with open(self.filename, "rb") as html_file:
            attachment = MIMEApplication(html_file.read(), _subtype="html")
            attachment.add_header(
                "Content-Disposition", "attachment", filename="report.html"
            )
            msg.attach(attachment)

        server = smtplib.SMTP_SSL("smtp.yandex.ru", 465)
        server.ehlo(login)

        server.login(
            login,
            password,
        )

        server.auth_plain()

        server.sendmail(
            login,
            receiver,
            msg.as_string(),
        )

        server.quit()
