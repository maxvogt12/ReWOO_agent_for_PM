import pm4py 

def Network_analysis_vis(file_path):
    log = pm4py.read_xes(file_path)
    df = pm4py.convert_to_dataframe(log)
    net_ana = pm4py.discover_network_analysis(df, out_column='case:concept:name', in_column='case:concept:name', node_column_source='org:resource', node_column_target='org:resource', edge_column='concept:name')
    pm4py.view_network_analysis(net_ana, format='svg')


if __name__ == "__main__":
    file_path = "/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/receipt.xes"
    Network_analysis_vis(file_path)

