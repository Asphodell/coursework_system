import re

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline
from plotly.subplots import make_subplots


class Visualizer:
    def __init__(self, df_t_u, df_t_t):
        self.df_t_u = df_t_u
        self.df_t_t = df_t_t

    def total_time_bar(self):
        df = self.df_t_t

        fig = px.pie(df, values='Total Time', names='User')

        fig.write_html("total_time.html")

    def users_graph(self):
        df = self.df_t_u

        x = []
        y = []

        fig = make_subplots()

        for i in range(len(df)):
            x.append(str(df['Begin Time'].loc[df.index[i]]))
            x.append(str(df['Expires Time'].loc[df.index[i]]))
            y.append(str(df['User'].loc[df.index[i]]))
            y.append(str(df['User'].loc[df.index[i]]))

            fig.add_trace(go.Scatter(x=x, y=y))

            x.clear()
            y.clear()
        fig.write_html("users_graph.html")
