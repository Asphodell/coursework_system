import argparse
import pathlib
from datetime import date

import floating_parser
import floating_statistics
import floating_visualizer
import floating_mail_sender
import floating_web


def main():

    #default_logs_path = pathlib.Path().cwd() / "tfs-log.txt"
    #argparser = argparse.ArgumentParser(description="Logs data to graphs")
    #argparser.add_argument(
    #    "-p",
    #    "--logs-path",
    #    action="store",
    #    dest="logs_file",
    #    required=True,
    #    default=default_logs_path,
    #    help=f"Full path to the Floating server logs file. Default path {default_logs_path}",
    #)
#
    #argparser.add_argument(
    #    "-s",
    #    "--send",
    #    action="store_true",
    #    help="Login, password and receiver should be in config.json",
    #)
#
    #args = argparser.parse_args()
#
    #file_path = args.logs_file
    
    file_path = ".\log_file1.txt"
    print(file_path)
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
    
    total_time_bar = vz.total_time_bar()
    users_graph = vz.users_graph()
    start_stop_graph = vz.start_stop_graph()

    #if args.send:
    #    snd = floating_mail_sender.Sender(
    #        "Report " + str(date.today()), "report " + str(date.today()) + ".html"
    #    )
    #    snd.send_mail()


    title = "Report " + str(date.today())
    app = floating_web.App(title, total_time_bar, users_graph, start_stop_graph)

    app.start_app() 

if __name__ == "__main__":
    main()
