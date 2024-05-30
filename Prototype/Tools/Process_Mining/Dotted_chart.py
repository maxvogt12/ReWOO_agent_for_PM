import pm4py
import pandas as pd

def dotted_chart_vis(event_log):
    # Loading event log as dataframe
    df = pm4py.convert_to_dataframe(event_log)
    # Visualizing dotted chart
    pm4py.view_dotted_chart(df, format='png')
    pm4py.view_dotted_chart(df, attributes=['time:timestamp', 'concept:name', 'org:resource'])
    
    return

if __name__ == "__main__":
    file_path = "/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/roadtraffic100traces.xes"
    event_log = pm4py.read_xes(file_path, return_legacy_log_object=True)
    dotted_chart_vis(event_log)