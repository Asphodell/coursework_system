import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

colors = px.colors.qualitative.Alphabet + px.colors.qualitative.Dark24 + px.colors.qualitative.Light24


class Visualizer:

    def __init__(self, df_t_u, df_t_t, df_s_s):
        self.df_t_u = df_t_u
        self.df_t_t = df_t_t
        self.df_s_s = df_s_s

    def total_time_bar(self):
        df = self.df_t_t

        df_with_color = self.one_user_one_color()

        fig = px.pie(df, values='Total Time', names='User', color_discrete_sequence=df_with_color['Color'])
        fig.write_html("total_time.html")

        return fig

    def one_user_one_color(self):
        df = self.df_t_t

        df = df.sort_values('Total Time', ascending=False)

        color_column = pd.DataFrame()
        for i in range(len(df)):
            color_column = pd.concat([pd.DataFrame([[colors[i]]]), color_column], ignore_index=True)

        df['Color'] = color_column

        return df

    def users_graph(self):
        df = self.df_t_u

        df_color = self.one_user_one_color()

        x = []
        y = []

        fig = make_subplots()

        for i in range(len(df)):
            x.append(str(df['Begin Time'].loc[df.index[i]]) + " " + df['Date'].loc[df.index[i]])
            x.append(str(df['End Time'].loc[df.index[i]]) + " " + df['Date'].loc[df.index[i]])
            y.append(str(df['User'].loc[df.index[i]]))
            y.append(str(df['User'].loc[df.index[i]]))

            fig.add_trace(go.Scatter(x=x, y=y, name=f'{y[0]}'))

            x.clear()
            y.clear()

        for i in range(len(df)):
            for j in range(len(df_color)):
                curr_name = fig['data'][i]['name']
                name = str(df_color['User'].loc[df_color.index[j]])
                if curr_name == name:
                    fig['data'][i]['line']['color'] = df_color['Color'].loc[df_color.index[j]]

        fig.update_layout(showlegend=False)
        fig.write_html("users_graph.html")
        return fig

    def start_stop_graph(self):
        df = self.df_s_s
        fig = px.scatter(df, x='Time', y='Process')

        fig.write_html("start_stop_graph.html")

        return fig

    def to_one(self):
        total_graph = self.total_time_bar()
        users_graph = self.users_graph()
        start_stop_graph = self.start_stop_graph()
        with open('result.html', 'a') as f:
            f.write(total_graph.to_html(full_html=False, include_plotlyjs='cdn'))
            f.write(users_graph.to_html(full_html=False, include_plotlyjs='cdn'))
            f.write(start_stop_graph.to_html(full_html=True, include_plotlyjs='cdn'))
