"""
The module is responsible for rendering data in an .html file
"""

from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class Visualizer:
    """
    The class contains data visualization methods
    """

    colors = (
        px.colors.qualitative.Alphabet
        + px.colors.qualitative.Dark24
        + px.colors.qualitative.Light24
    )  # count of colors: 74

    def __init__(self, df_t_time_and_user: pd.DataFrame, df_total_time: pd.DataFrame, df_start_and_stop: pd.DataFrame):
        self.df_time_and_user = df_t_time_and_user
        self.df_total_time = df_total_time
        self.df_start_and_stop = df_start_and_stop

    def total_time_bar(self) -> px.pie:
        """
        Build pie chart to compare total time spent
        """

        df = self.df_total_time

        df_with_color = self.one_user_one_color()

        fig = px.pie(
            df,
            values="Total Time",
            names="User",
            color_discrete_sequence=df_with_color["Color"],
        )

        fig.write_html("total_time.html")

        return fig

    def total_time_altair(self) -> px.bar:
        """
        Build altair chart to compare total time spent
        """

        df = self.df_total_time

        df_with_color = self.one_user_one_color()

        fig = px.bar(
            df, x="User", y="Total Time", color_discrete_sequence=df_with_color["Color"]
        )

        fig.write_html("total_time_altair.html")

        return fig

    def one_user_one_color(self) -> pd.DataFrame:
        """
        Assigns a unique color to each user
        """

        df = self.df_total_time

        df = df.sort_values("Total Time", ascending=False)

        color_column = pd.DataFrame()
        for i in range(len(df)):
            color_column = pd.concat(
                [pd.DataFrame([[self.colors[i]]]), color_column], ignore_index=True
            )

        df["Color"] = color_column

        return df

    def users_graph(self) -> go.Figure:
        """
        Building a linear graph to track a specific point in time of use
        """

        df = self.df_time_and_user

        df_color = self.one_user_one_color()

        x = []
        y = []

        fig = make_subplots()

        for i in range(len(df)):
            x.append(
                str(df["Begin Time"].loc[df.index[i]])
                + " "
                + df["Date"].loc[df.index[i]]
            )
            x.append(
                str(df["End Time"].loc[df.index[i]]) + " " + df["Date"].loc[df.index[i]]
            )
            y.append(str(df["User"].loc[df.index[i]]))
            y.append(str(df["User"].loc[df.index[i]]))

            fig.add_trace(go.Scatter(x=x, y=y, name=f"{y[0]}"))

            x.clear()
            y.clear()

        for i in range(len(df)):
            for j in range(len(df_color)):
                curr_name = fig["data"][i]["name"]
                name = str(df_color["User"].loc[df_color.index[j]])
                if curr_name == name:
                    fig["data"][i]["line"]["color"] = df_color["Color"].loc[
                        df_color.index[j]
                    ]

        fig.update_layout(showlegend=False)
        fig.write_html("users_graph.html")
        return fig

    def start_stop_graph(self) -> px.scatter:
        """
        Plots the tracking of activation and deactivation points
        """

        df = self.df_start_and_stop
        fig = px.scatter(df, x="Time", y="Process")

        fig.write_html("start_stop_graph.html")

        return fig

    def to_one(self):
        """
        Combines the generated graphics into a single .html file
        """

        total_graph = self.total_time_bar()
        users_graph = self.users_graph()
        start_stop_graph = self.start_stop_graph()
        date_today = str(date.today())
        with open(f"report {date_today}" + ".html", "a", encoding="utf-8") as f:
            f.write(total_graph.to_html(full_html=False, include_plotlyjs="cdn"))
            f.write(users_graph.to_html(full_html=False, include_plotlyjs="cdn")) 
            f.write(start_stop_graph.to_html(full_html=True, include_plotlyjs="cdn"))
