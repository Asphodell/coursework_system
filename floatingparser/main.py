'''
Starting the Data Analytics System
'''

import argparse
import pathlib
from datetime import date
import os
import sys

from .floating_parser import LogParser
from .floating_statistics import Statistics
from .floating_visualizer import Visualizer
from .floating_mail_sender import Sender
from .floating_web import App


def FloatingStart():
    '''
    Working with modules
    '''

    default_logs_path = pathlib.Path().cwd() / "tfs-log.txt"
    argparser = argparse.ArgumentParser(description="Logs data to graphs")
    
    argparser.add_argument(
        "-s",
        "--send",
        action="store_true",
        help="Send report to mail. Login, password and receiver should be in config.json",
    )

    argparser.add_argument(
        "-w",
        "--web",
        action="store_true",
        help=f"Open web app where user can interact with graphs. Use full path to the Floating server logs file. Default path {default_logs_path}", 
    )

    argparser.add_argument(
        "-p",
        "--logs-path",
        action="store",
        dest="logs_file",
        required=True,
        default=default_logs_path,
        help=f"Full path to the Floating server logs file. Default path {default_logs_path}",
    )

    args = argparser.parse_args()

    file_path = args.logs_file

    lp = LogParser(file_path)
    df = lp.build_df()

    st = Statistics(df)

    df_time_user = st.create_df_time_and_user()
    df_total_time = st.create_df_total_time()
    df_start_stop = st.create_df_start_and_stop()

    vz = Visualizer(
        df_time_user,
        df_total_time,
        df_start_stop,
    )

    vz.to_one()

    total_time_bar = vz.total_time_bar()
    total_time_altair = vz.total_time_altair()
    users_graph = vz.users_graph()
    start_stop_graph = vz.start_stop_graph()

    if args.send:
        snd = Sender(
            "Report " + str(date.today()), "report " + str(date.today()) + ".html"
        )
        snd.send_mail()

    title = "Report " + str(date.today())
    app = App(title,
                            total_time_bar, 
                            users_graph, 
                            start_stop_graph, 
                            total_time_altair
                            )

    app.start_app() 

    if args.web:
        file_name = sys.argv[0]
        os.system(rf'streamlit run {file_name} -- -p {file_path}')

if __name__ == "__main__":
    FloatingStart()
