import pm4py 

from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.visualization.bpmn import visualizer as bpmn_visualizer
from pm4py.discovery import discover_dfg


class ProcessMiner:

    def __init__(self, pm_df):
        self.pm_df = pm_df[0:10]
        self.pm_log = pm4py.format_dataframe(self.pm_df,
                                            case_id='User', 
                                            activity_key='Action',
                                            timestamp_key='Datetime')

        self.net, self.initial_marking, self.final_marking = alpha_miner.apply(self.pm_log)


    def build_alplha_miner(self):
        net = self.net
        initial_marking = self.initial_marking
        final_marking = self.final_marking

        gviz = pn_visualizer.apply(net, initial_marking, final_marking)

        pn_visualizer.view(gviz)

        pn_visualizer.save(gviz, "alpha_miner.png")

    def build_bpmn(self):
        net = self.net
        initial_marking = self.initial_marking
        final_marking = self.final_marking

        bpmn_graph = pm4py.convert_to_bpmn(net, initial_marking, final_marking)

        gviz = bpmn_visualizer.apply(bpmn_graph)

        bpmn_visualizer.view(gviz)

        bpmn_visualizer.save(gviz, 'bpmn.png')

    def build_dfg(self):
        pm_log = self.pm_log

        dfg, start_activities, end_activities = discover_dfg(pm_log)

        pm4py.view_dfg(dfg, start_activities=start_activities, end_activities=end_activities)
