import argparse
import json
import pathlib
from datetime import date

import floating_parser
import floating_statistics
import floating_visualizer

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib


def main():
    default_logs_path = pathlib.Path().cwd() / "tfs-log.txt"
    argparser = argparse.ArgumentParser(description="Logs data to graphs")
    argparser.add_argument("-p", "--logs-path",
                           action="store",
                           dest="logs_file",
                           required=True,
                           default=default_logs_path,
                           help=f"Full path to the Floating server logs file. Default path {default_logs_path}")

    argparser.add_argument("-s", "--send",
                           action="store_true",
                           help="Login, password and receiver should be in config.json")

    args = argparser.parse_args()

    file_path = args.logs_file
    lp = floating_parser.LogParser(file_path)
    df = lp.build_df()

    st = floating_statistics.Statistics(df)

    df_time_user = st.create_df_time_and_user()
    df_total_time = st.create_df_total_time()
    df_start_stop = st.create_df_start_and_stop()

    vz = floating_visualizer.Visualizer(
        df_time_user,
        df_total_time,
        df_start_stop,
    )

    vz.to_one()

    if args.send:
        send_mail('Report ' + str(date.today()), 'report ' + str(date.today()) + '.html')


def send_mail(subject, filename):
    with open('config.json', 'r') as file:
        data = json.load(file)

    login = data['login']
    password = data['password']
    receiver = data['receiver']

    msg = MIMEMultipart()
    msg['From'] = login
    msg['To'] = receiver
    msg['Subject'] = subject

    with open(filename, 'rb') as html_file:
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


if __name__ == "__main__":
    main()
