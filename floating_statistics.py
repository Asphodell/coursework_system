import re

import numpy as np
import pandas as pd


class Statistics:
    def __init__(self, df_log):
        self.df_log = df_log

    def time_and_user(self):  # only ONE checking str in many functions ?? (before all functions)
        df_log = self.df_log[::-1].reset_index(drop=True)
        df_time_and_user = pd.DataFrame()

        for i in range(len(df_log)):

            checking_str = df_log['Action'].loc[df_log.index[i]]
            expires_time = re.search(r"\d\d:\d\d:\d\d", checking_str)

            if expires_time != None:
                begin_time = df_log['Time'].loc[df_log.index[i]]
                username = re.sub(r"[\W\d+]", "", re.search(r"\(.*?\)", checking_str)[0])

                df_time_and_user = pd.concat(
                    [pd.DataFrame([[begin_time, expires_time[0], username]]), df_time_and_user], ignore_index=True)

        df_time_and_user.rename(columns={0: "Begin Time", 1: "Expires Time", 2: "User"}, inplace=True)

        # df_time_and_user.index = np.arange(1, len(df_time_and_user) + 1)

        return df_time_and_user

    def total_time(self):
        df = self.time_and_user()
        users = df['User'].value_counts()
        df = df.drop_duplicates(subset=['User'])
        df.reset_index(drop=True, inplace=True)

        column = pd.DataFrame()

        df_total_btime = pd.DataFrame()
        df_total_etime = pd.DataFrame()

        for i in range(len(df)):
            bhours = int(str(df["Begin Time"].loc[df.index[i]])[:2])
            bminutes = int(str(df["Begin Time"].loc[df.index[i]])[3:5])
            bseconds = int(str(df["Begin Time"].loc[df.index[i]])[6:8])
            total_btime = (bhours * 60 * 60) + (bminutes * 60) + bseconds

            ehours = int(str(df["Expires Time"].loc[df.index[i]])[:2])
            eminutes = int(str(df["Expires Time"].loc[df.index[i]])[3:5])
            eseconds = int(str(df["Expires Time"].loc[df.index[i]])[6:8])
            total_etime = (ehours * 60 * 60) + (eminutes * 60) + eseconds

            df_total_btime = pd.concat([pd.DataFrame([[total_btime]]), df_total_btime])[::-1]
            df_total_etime = pd.concat([pd.DataFrame([[total_etime]]), df_total_etime])[::-1]

        df_total_btime = df_total_btime.reset_index(drop=True)
        df['BeginSec'] = df_total_btime

        df_total_etime = df_total_etime.reset_index(drop=True)
        df['ExpSec'] = df_total_etime

        total_time = 0

        print(len(users))

        for j in range(len(df) - 1):
            if df['ExpSec'].loc[df.index[j]] < df['BeginSec'].loc[df.index[j + 1]]:
                total_time += (df['BeginSec'].loc[df.index[j + 1]] - df['BeginSec'].loc[df.index[j]])
                column = pd.concat([pd.DataFrame([[total_time]]), column])[::-1]
            else:
                total_time += 30

            print(total_time)

        column = column.reset_index(drop=True)
        df['Total Time'] = column
        print(df)
        # for i in range(len(users)):
        #    total_time = users[i] * 30

        # df.pop('Begin Time')
        # df.pop('Expires Time')
#
# df.index = np.arange(1, len(df) + 1)
#
# return df