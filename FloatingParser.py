import numpy as np
import pandas as pd


class LogParser:
    def __init__(self, path_log):
        self.path_log = path_log

    def build_df(self):
        df_log = pd.DataFrame()

        with open(self.path_log, "r") as f:
            lines = f.readlines()
            for line in lines:
                current_line = line.strip()
                date_time_type = current_line.split(" ")[0:3]
                action = " ".join(current_line.split(" ")[3:])

                if len(date_time_type) == 3:
                    date = str(np.array(date_time_type[0][:-1]))
                    timE = np.array(date_time_type[1])
                    type = np.array(date_time_type[2][:-1])

                df_log = pd.concat([pd.DataFrame([[date, timE, type, action]]), df_log], ignore_index=True)

        df_log.rename(columns={0: 'Date', 1: 'Time', 2: 'Type', 3: 'Action'}, inplace=True)
        df_log = df_log[::-1].reset_index(drop=True)

        df_log.index = np.arange(1, len(df_log) + 1)

        return df_log
