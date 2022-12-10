import re
from datetime import datetime
import numpy as np
import pandas as pd


class Statistics:
    def __init__(self, df_log):
        self.df_log = df_log

    def time_and_user(self):
        df_log = self.df_log[::-1].reset_index(drop=True)
        df_time_and_user = pd.DataFrame()

        for i in range(len(df_log)):

            checking_str = df_log['Action'].loc[df_log.index[i]]
            expires_time = re.search(r"\d\d:\d\d:\d\d", checking_str)

            if expires_time is not None:
                begin_time = df_log['Time'].loc[df_log.index[i]]
                username = re.sub(r"[\W\d+]", "", re.search(r"\(.*?\)", checking_str)[0])

                df_time_and_user = pd.concat(
                    [pd.DataFrame([[begin_time, expires_time[0], username]]), df_time_and_user], ignore_index=True)

        df_time_and_user.rename(columns={0: "Begin Time", 1: "Expires Time", 2: "User"}, inplace=True)

        df_time_and_user.index = np.arange(1, len(df_time_and_user) + 1)


        return df_time_and_user

    def total_time(self):
        df = self.time_and_user()
        df1 = df

        df = df.drop_duplicates(subset=['User'], keep='last')
        df1 = df1.drop_duplicates(subset=['User'])

        df = df.sort_values(by='User')
        df1 = df1.sort_values(by='User')

        df.reset_index(drop=True, inplace=True)
        df1.reset_index(drop=True, inplace=True)

        fmt = '%H:%M:%S'

        column = pd.DataFrame()

        for i in range(len(df)):
            tdelta = datetime.strptime(str(df['Expires Time'].loc[df.index[i]]), fmt) - datetime.strptime(
                str(df1['Begin Time'].loc[df1.index[i]]), fmt)

            a = re.search(r"\d+:\d\d:\d\d", str(tdelta))
            sec = abs(tdelta.total_seconds())
            d_t_obj = datetime.strptime(str(a[0]), '%H:%M:%S')
            total = int(d_t_obj.strftime('%S'))
            total += int(d_t_obj.strftime('%M')) * 60
            total += int(d_t_obj.strftime('%H')) * 60 * 60
            total2 = total + sec + total
            column = pd.concat([pd.DataFrame([[total2]]), column], ignore_index=True)

        column = column[::-1].reset_index(drop=True)

        df['Total Time'] = column

        df = df.drop(columns=['Begin Time', 'Expires Time'])

        return df

    def start_stop(self):
        df = self.df_log
        df_start_stop = pd.DataFrame()

        for i in range(len(df)):
            checking_str = df['Action'].loc[df.index[i]]
            time = df['Time'].loc[df.index[i]]

            pattern_act = 'Activated successfully.'
            pattern_deact = 'Deactivated successfully.'
            activation = re.search(pattern_act, checking_str)
            deactivation = re.search(pattern_deact, checking_str)

            if deactivation is not None:
                df_start_stop = pd.concat(
                    [pd.DataFrame([[time, deactivation[0]]]), df_start_stop], ignore_index=True)

            if activation is not None:
                df_start_stop = pd.concat(
                    [pd.DataFrame([[time, activation[0]]]), df_start_stop], ignore_index=True)

        df_start_stop = df_start_stop[::-1].reset_index(drop=True)
        df_start_stop.rename(columns={0: "Time", 1: "Process"}, inplace=True)

        return df_start_stop
