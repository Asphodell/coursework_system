import argparse
import pathlib
import floating_parser
import floating_statistics

default_logs_path = pathlib.Path().cwd() / "my_file.txt"
argparser = argparse.ArgumentParser()
argparser.add_argument("-p", "--logs-path",
                       action="store",
                       dest="logs_file",
                       required=True,
                       default=default_logs_path,
                       help=f"Full path to the Floating server logs file. Default path {default_logs_path}")
args = argparser.parse_args()

file_path = args.logs_file


def main():
    lp = floating_parser.LogParser(file_path)
    df = lp.build_df()
    st = floating_statistics.Statistics(df)
    print(lp.build_df())
    print(st.time_and_user())
    print(st.total_time())


if __name__ == "__main__":
    main()
