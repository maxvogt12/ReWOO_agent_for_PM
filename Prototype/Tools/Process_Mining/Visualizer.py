import pm4py
from General_Settings import Visualizations_Setting


# Function for process model visualization
def model_visualizer(event_log):

    #Visualization settings
    vis_BPMN = Visualizations_Setting.BPMN
    vis_Petri = Visualizations_Setting.Petri
    vis_DFG = Visualizations_Setting.DFG
    vis_tree = Visualizations_Setting.Decision_tree
    vis_Heuristic = Visualizations_Setting.Heuristic

    # Visualizing generated BPMN model
    if vis_BPMN == True:
        process_tree = pm4py.discover_process_tree_inductive(event_log)
        bpmn_model = pm4py.convert_to_bpmn(process_tree)
        pm4py.view_bpmn(bpmn_model)

    # Visualizing Petri net
    if vis_Petri == True:
        net, im, fm = pm4py.discover_petri_net_ilp(event_log)
        pm4py.view_petri_net(net, im, fm)

    # Visualizing DFG
    if vis_DFG == True:
        dfg, start_activities, end_activities = pm4py.discover_dfg(event_log)
        pm4py.view_dfg(dfg, start_activities, end_activities)

    # Visualizing decision tree
    if vis_tree == True:
        process_tree = pm4py.discover_process_tree_inductive(event_log)
        pm4py.view_process_tree(process_tree)

    # Visualizing heuristic net
    if vis_Heuristic == True:
        heuristic = pm4py.discover_heuristics_net(event_log)
        pm4py.view_heuristics_net(heuristic)

    return True