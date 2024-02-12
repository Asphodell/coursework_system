"""
The module is responsible for creating a web application
"""

import streamlit as st


class App:
    """
    Application
    """

    def __init__(self, title, fig_total_time, fig_users_graph, fig_start_stop_graph):
        self.title = title

        self.fig_total_time = fig_total_time
        self.users_graph = fig_users_graph
        self.fig_start_stop_graph = fig_start_stop_graph

    def write_title(self):
        """
        Title Placement
        """

        title = self.title

        st.title(title)

    def add_total_time_bar(self):
        """
        Placing pie chart on the application page
        """

        fig = self.fig_total_time

        st.write(
            "Pie diagram, where you can see how much time each user spent during the reporting period"
        )

        st.plotly_chart(fig)

    def add_users_graph(self):
        """
        Placing a User Monitoring Schedule on the Application Page
        """

        fig = self.users_graph

        st.write(
            "Here you can track the user's activity in a specific period of time. \
            The line shows the duration of the session, \
            and from below you can see the specific time of the user."
        )

        st.plotly_chart(fig)

    def add_start_stop_graph(self):
        '''
        Posting the Activation and Deactivation Tracking Schedule
        '''

        fig = self.fig_start_stop_graph

        st.write(
            "These points indicate the activation and deactivation times.\
            Using the graph, it is convenient to track a specific time."
        )

        st.plotly_chart(fig)

    def start_app(self):
        '''
        Placing Objects on an Application Page
        '''

        self.write_title()

        self.add_total_time_bar()
        self.add_users_graph()
        self.add_start_stop_graph()
