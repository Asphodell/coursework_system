import argparse
import pathlib

import FloatingParser
import FloatingStatistics
import FloatingVisualizer

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib

import config


def main():
    default_logs_path = pathlib.Path().cwd() / "tfs-log.txt"
    argparser = argparse.ArgumentParser(description="Logs data to graphs")
    argparser.add_argument("-p", "--logs-path",
                           action="store",
                           dest="logs_file",
                           required=True,
                           default=default_logs_path,
                           help=f"Full path to the Floating server logs file. Default path {default_logs_path}")

    args = argparser.parse_args()

    file_path = args.logs_file
    lp = FloatingParser.LogParser(file_path)
    df = lp.build_df()

    st = FloatingStatistics.Statistics(df)

    df_time_user = st.time_user()
    df_total_time = st.total_time()
    df_start_stop = st.start_stop()

    vz = FloatingVisualizer.Visualizer(df_time_user, df_total_time, df_start_stop)
    # vz.users_graph()
    # vz.total_time_bar()
    # vz.start_stop_graph()
    vz.to_one()


def send_mail(to_addr, subject, filename):
    sender = config.login
    password = config.password

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to_addr
    msg['Subject'] = subject

    with open(filename, 'rb') as html_file:
        attachment = MIMEApplication(html_file.read(), _subtype='html')
        attachment.add_header('Content-Disposition', 'attachment', filename="result.html")
        msg.attach(attachment)

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.ehlo(sender)

    server.login(sender, password)
    server.auth_plain()

    server.sendmail(sender, to_addr, msg.as_string())

    server.quit()


if __name__ == "__main__":
    main()
