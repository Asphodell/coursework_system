"""
The module is responsible for creating a web application
"""

import streamlit as st


class App:
    """
    Application
    """

    def __init__(self, title, fig_total_time, fig_users_graph, fig_start_stop_graph, fig_total_time_altair):
        self.title = title

        self.fig_total_time = fig_total_time
        self.users_graph = fig_users_graph
        self.fig_start_stop_graph = fig_start_stop_graph
        self.fig_total_time_altair = fig_total_time_altair

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

        st.subheader("Total time (pie chart)", divider="rainbow")

        fig = self.fig_total_time

        st.write(
            "Pie diagram, where you can see how much time each user spent during the reporting period"
        )

        st.plotly_chart(fig)

    def add_altair_bar(self):
        """
        Placing altair bar on the application page
        """

        st.subheader("Total time (bar chart)", divider="rainbow")

        fig = self.fig_total_time_altair

        st.write("Bar chart, where you can see how much time each user spent during the reporting period")

        st.plotly_chart(fig)

    def add_users_graph(self):
        """
        Placing a User Monitoring Schedule on the Application Page
        """

        st.subheader("Users graph", divider='rainbow')

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

        st.subheader("Start and stop graph", divider="rainbow")

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

        page = st.sidebar.selectbox("Choose page", 
                            ["Total time", 
                            "Users graph",
                            "Start and stop graph",
                            "Summarized report"])

        self.write_title()

        if page == "Total time":
            self.add_total_time_bar()

            self.add_altair_bar() 

        if page == "Users graph":
            self.add_users_graph()

        if page == "Start and stop graph":
            self.add_start_stop_graph()
        
        if page == "Summarized report":
            self.add_total_time_bar()
            st.divider()

            self.add_altair_bar()
            st.divider()

            self.add_users_graph()
            st.divider()

            self.add_start_stop_graph()
