import re

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

                df_time_and_user = pd.concat([pd.DataFrame([[begin_time, expires_time[0], username]]), df_time_and_user], ignore_index=True)

        df_time_and_user.rename(columns={0: "Begin Time", 1: "Expires Time", 2: "User"}, inplace=True)

        return df_time_and_user

    def total_time(self):
        df = self.time_and_user()
        users = df['User'].value_counts() #.to_frame()
        df = df.drop_duplicates(subset=['User'])
        df.reset_index(drop=True, inplace=True)
        column = pd.DataFrame()
        for i in range(len(users)):
            total_time = users[i] * 30
            #print(total_time, users[i] * 30)
            column = pd.concat([pd.DataFrame([[total_time]]), column])[::-1]
        column = column.reset_index(drop=True)
        df['Total Time'] = column
        df.pop('Begin Time')
        df.pop('Expires Time')
        return df