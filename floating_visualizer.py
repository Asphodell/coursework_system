import re

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline
from plotly.subplots import make_subplots


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

        df1 = df
        df1 = df1.drop_duplicates(subset='User')

        x = []
        y = []

        fig = make_subplots()

        for i in range(len(df)):
            x.append(str(df['Begin Time'].loc[df.index[i]]))
            x.append(str(df['Expires Time'].loc[df.index[i]]))
            y.append(str(df['User'].loc[df.index[i]]))
            y.append(str(df['User'].loc[df.index[i]]))

            trace = fig.add_trace(go.Scatter(x=x, y=y, name=f'{y[0]}'))

            x.clear()
            y.clear()

        colors = ['aqua', 'aquamarine',
            'beige', 'bisque', 'black', 'blanchedalmond', 'blue',
            'blueviolet','brown', 'burlywood', 'cadetblue',
            'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
            'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan',
            'darkgoldenrod', 'darkgreen',
            'darkkhaki', 'darkolivegreen', 'darkorange',
            'darkorchid', 'darkred', 'darksalmon', 'darkseagreen',
            'darkslateblue','darkslategray', 'darkslategrey',
            'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue',
            'dimgray', 'dimgrey', 'dodgerblue', 'firebrick',
            'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro',
            'ghostwhite', 'gold', 'goldenrod', 'gray', 'grey', 'green',
            'greenyellow', 'honeydew', 'hotpink', 'indigo',
            'ivory', 'khaki', 'lavender', 'lavenderblush', 'lightyellow', 'lime',
            'magenta','maroon', 'mistyrose', 'moccasin', 'navajowhite', 'navy',
            'oldlace', 'olive', 'olivedrab', 'orange', 'orangered',
            'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise',
            'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink',
            'plum', 'powderblue', 'purple', 'red', 'rosybrown',
            'royalblue', 'rebeccapurple', 'saddlebrown', 'salmon',
            'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver',
            'skyblue', 'slateblue', 'slategrey', 'snow',
            'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato',
            'turquoise', 'violet', 'wheat', 'white', 'whitesmoke',
            'yellow']

        for i in range(len(df)):
            for j in range(len(df1)):
                curr_name = fig['data'][i]['name']
                name = str(df1['User'].loc[df1.index[j]])
                if curr_name == name:
                    fig['data'][i]['line']['color'] = colors[j]

        fig.update_layout(showlegend=False)
        fig.write_html("users_graph.html")

    def start_stop_graph(self):
        df = self.df_s_s
