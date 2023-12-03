import json
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib

class Sender:
    def __init__(self, subject, filename):
        self.subject = subject
        self.filename = filename
        
    def send_mail(self):
        with open('config.json', 'r') as file:
            data = json.load(file)

        login = data['login']
        password = data['password']
        receiver = data['receiver']

        msg = MIMEMultipart()
        msg['From'] = login
        msg['To'] = receiver
        msg['Subject'] = self.subject

        with open(self.filename, 'rb') as html_file:
            attachment = MIMEApplication(html_file.read(), _subtype='html')
            attachment.add_header('Content-Disposition', 'attachment', filename="report.html")
            msg.attach(attachment)

        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
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
