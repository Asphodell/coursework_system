import argparse
import pathlib
import LogParser

parser = argparse.ArgumentParser()
parser.add_argument("log_name")
arg = parser.parse_args()
path_log = pathlib.Path(arg.log_name)

if __name__ == "__main__":
    lp = LogParser.LogParser(path_log)
    print(lp.build_df())