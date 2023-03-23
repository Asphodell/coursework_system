import re
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline
from plotly.subplots import make_subplots
import Colors


class Visualizer:

    def __init__(self, df_t_u, df_t_t, df_s_s):
        self.df_t_u = df_t_u
        self.df_t_t = df_t_t
        self.df_s_s = df_s_s

    def total_time_bar(self):
        df = self.df_t_t

        fig = px.pie(df, values='Total Time', names='User')
        fig.write_html("total_time.html")

    def users_graph(self):
        df = self.df_t_u
        colors = Colors.ColorPalette()

        df1 = df
        df1 = df1.drop_duplicates(subset='User')

        x = []
        y = []

        fig = make_subplots()

        for i in range(len(df)):
            x.append(str(df['Begin Time'].loc[df.index[i]]) + " " + df['Date'].loc[df.index[i]])
            x.append(str(df['End Time'].loc[df.index[i]]) + " " + df['Date'].loc[df.index[i]])
            y.append(str(df['User'].loc[df.index[i]]))
            y.append(str(df['User'].loc[df.index[i]]))

            trace = fig.add_trace(go.Scatter(x=x, y=y, name=f'{y[0]}'))

            x.clear()
            y.clear()

        for i in range(len(df)):
            for j in range(len(df1)):
                curr_name = fig['data'][i]['name']
                name = str(df1['User'].loc[df1.index[j]])
                if curr_name == name:
                    fig['data'][i]['line']['color'] = colors.colors[j]

        fig.update_layout(showlegend=False)
        fig.write_html("users_graph.html")

    def start_stop_graph(self):
        df = self.df_s_s
        fig = px.scatter(df, x='Time', y='Process')
        fig.write_html("start_stop.html")
