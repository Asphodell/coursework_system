"""
This module selects smaller ones from the general dataframe, selecting the desired parameters
"""

import re
import datetime
import pandas as pd


class Statistics:
    """
    This class contains three methods of data selection
    """

    def __init__(self, df_log: pd.DataFrame):
        self.df_log = df_log

    def create_df_time_and_user(self) -> pd.DataFrame:
        """
        The function tracks for each user their time spent
        """

        df_log = self.df_log[::-1].reset_index(drop=True)
        df_time_user = pd.DataFrame()
        end_time_column = pd.DataFrame()

        for i in range(len(df_log)):
            checking_str = df_log["Action"].loc[df_log.index[i]]
            new_lease = "New lease assigned"
            release_lease = "Lease was released"
            expired_lease = "Lease has expired"
            deactivated = "Failed to activate"

            if new_lease in checking_str:
                username = re.search(r"\(.*?\)", checking_str).group(0)
                username = re.sub(r"[()]", "", username)
                begin_time = df_log["Time"].loc[df_log.index[i]]
                date = df_log["Date"].loc[df_log.index[i]]
                df_time_user = pd.concat(
                    [pd.DataFrame([[date, username, begin_time]]), df_time_user],
                    ignore_index=True,
                )

            if expired_lease in checking_str or release_lease in checking_str:
                username = re.search(r"\(.*?\)", checking_str).group(0)
                username = re.sub(r"[()]", "", username)
                end_time = df_log["Time"].loc[df_log.index[i]]
                end_time_column = pd.concat(
                    [pd.DataFrame([[username, end_time]]), end_time_column],
                    ignore_index=True,
                )

            if deactivated in checking_str:
                username = ""
                end_time = df_log["Time"].loc[df_log.index[i]]
                end_time_column = pd.concat(
                    [pd.DataFrame([[username, end_time]]), end_time_column],
                    ignore_index=True,
                )

        df_time_user.rename(
            columns={0: "Date", 1: "User", 2: "Begin Time"}, inplace=True
        )
        end_time_column.rename(columns={0: "User", 1: "End time"}, inplace=True)
        df_time_user["End Time"] = end_time_column["End time"]

        return df_time_user

    def create_df_total_time(self) -> pd.DataFrame:
        """ 
        The function calculates the total time spent by each user
        """

        df = self.create_df_time_and_user()
        difference_column = pd.DataFrame()
        total = 0

        for i in range(len(df)):
            difference = datetime.datetime.strptime(
                str(df["End Time"].loc[df.index[i]]), "%H:%M:%S"
            ) - datetime.datetime.strptime(
                str(df["Begin Time"].loc[df.index[i]]), "%H:%M:%S"
            )
            if difference.total_seconds() < 0:
                difference = (24 * 60 * 60) + difference.total_seconds()
            else:
                difference = difference.total_seconds()
            difference_column = pd.concat(
                [pd.DataFrame([[difference]]), difference_column], ignore_index=True
            )

        difference_column = difference_column[::-1].reset_index(drop=True)
        df["Diff"] = difference_column
        df = df.rename_axis("index")
        df = df.sort_values(by=["User", "index"])

        total_column = pd.DataFrame()

        for i in range(len(df) - 1):
            if df["User"].loc[df.index[i]] == df["User"].loc[df.index[i + 1]]:
                total += df["Diff"].loc[df.index[i]] + df["Diff"].loc[df.index[i]]
            else:
                total_column = pd.concat(
                    [pd.DataFrame([[total]]), total_column], ignore_index=True
                )
                total = 0

        df = df.groupby("User").sum(numeric_only=True)
        df = df.reset_index()
        df = df.rename(columns={"Diff": "Total Time"})

        return df

    def create_df_start_and_stop(self) -> pd.DataFrame:
        '''
        The function defines the activation and deactivation points
        '''

        df = self.df_log
        df_start_stop = pd.DataFrame()

        for i in range(len(df)):
            checking_str = df["Action"].loc[df.index[i]]
            time = (
                str(df["Time"].loc[df.index[i]])
                + " "
                + str(df["Date"].loc[df.index[i]])
            )

            pattern_act = "Activated successfully."
            pattern_deact = "Deactivated successfully."
            activation = re.search(pattern_act, checking_str)
            deactivation = re.search(pattern_deact, checking_str)

            if deactivation is not None:
                df_start_stop = pd.concat(
                    [pd.DataFrame([[time, deactivation[0]]]), df_start_stop],
                    ignore_index=True,
                )

            if activation is not None:
                df_start_stop = pd.concat(
                    [pd.DataFrame([[time, activation[0]]]), df_start_stop],
                    ignore_index=True,
                )

        df_start_stop = df_start_stop[::-1].reset_index(drop=True)
        df_start_stop.rename(columns={0: "Time", 1: "Process"}, inplace=True)

        return df_start_stop
