import numpy as np
import pandas as pd

class LogParser():
    def __init__(self, path_log):
        self.path_log = path_log

    def build_df(self):
        log = open(self.path_log)
        df_log = pd.DataFrame()
        df_log.rename(columns={0: 'Date', 1: 'Time', 2: 'Type', 3: 'Action'}, inplace=True)
        count_lines = 0
        while True:
            current_line = log.readline()
            count_lines += 1

            date_time_type = current_line.split(" ")[0:3]
            action_array = current_line.split(" ")[3:]
            action = " ".join(action_array)

            if len(date_time_type) == 3:
               date = np.array(date_time_type[0][:-1])
               timE = np.array(date_time_type[1])
               type = np.array(date_time_type[2][:-1])

            added_row = {'Date': date, 'Time': timE, 'Type': type, 'Action': action}
            df_log = df_log.append(added_row, ignore_index=True)

            if not current_line:
                break
        return df_log
