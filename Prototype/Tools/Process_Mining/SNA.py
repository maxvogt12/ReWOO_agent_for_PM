import pm4py 

def SNA_vis(file_path):
    log = pm4py.read_xes(file_path)
    df = pm4py.convert_to_dataframe(log)
    metric = pm4py.discover_subcontracting_network(df, resource_key='org:resource', timestamp_key='time:timestamp', case_id_key='case:concept:name')
    pm4py.view_sna(metric)


if __name__ == "__main__":
    file_path = "/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/receipt.xes"
    file_path = "/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/review_example_large.xes"
    SNA_vis(file_path)