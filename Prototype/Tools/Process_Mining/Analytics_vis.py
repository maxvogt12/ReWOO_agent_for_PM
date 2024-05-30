import pm4py
import pandas as pd
from .CSV_config import CSV_format
from General_Settings import Analytics_Settings
from .Dotted_chart import dotted_chart_vis




# from CSV_config import CSV_format
# import sys
# sys.path.append('/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Prototype/')

# # Now you can import modules from this directory
# from General_Settings import Analytics_Settings


def analytics_visualizer(event_log, file_type):
    df = pm4py.convert_to_dataframe(event_log)
    print(df.head)

    # Vis settings
    event_dis = Analytics_Settings.event_distribution
    event_time = Analytics_Settings.event_time
    case_duration = Analytics_Settings.case_duration
    sna = Analytics_Settings.SNA
    dotted_chart = Analytics_Settings.Dotted_chart

    if file_type == "csv":
    # General formatting setting
        activity_key = CSV_format.activity
        case_id_key = CSV_format.case
        timestamp_key = CSV_format.timestamp
        resource_key = ''
    elif file_type == "xes":
        activity_key = 'concept:name'
        case_id_key = 'case:concept:name'
        timestamp_key = 'time:timestamp'
        resource_key = 'org:resource'
    else:
        return

    if event_dis == True:
    # View distribution of events per day of the week
        pm4py.view_events_distribution_graph(df, format='png', distr_type='days_week', activity_key=activity_key, case_id_key=case_id_key, timestamp_key=timestamp_key)

    if event_time == True:
    # View event per time graph
        pm4py.view_events_per_time_graph(df, format='png', activity_key=activity_key, case_id_key=case_id_key, timestamp_key=timestamp_key)

    if case_duration == True:
    # View case duration
        pm4py.view_case_duration_graph(df, format='png', activity_key=activity_key, case_id_key=case_id_key, timestamp_key=timestamp_key)

    if sna == True:
    # View SNA
        metric = pm4py.discover_subcontracting_network(df, resource_key=resource_key, timestamp_key=timestamp_key, case_id_key=case_id_key)
        pm4py.view_sna(metric)

    if dotted_chart == True:
        dotted_chart_vis(event_log)

    return

if __name__ == "__main__":
    file_path = "/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/review_example_large.xes"
    if "csv" in file_path:
      # For CSV file formats paramters for 3 columns have to be set manually here
      df = pd.read_csv(file_path, sep=',')

      # If required, convert time format
      df['timestamp'] = pd.to_datetime(df['timestamp'])

      df = pm4py.format_dataframe(df, case_id='case_id', activity_key='activity', timestamp_key='timestamp')
      event_log = pm4py.convert_to_event_log(df)
    else:
      # Reading the event log directly from XES file
      event_log = pm4py.read_xes(file_path)

    analytics_visualizer(event_log, "xes")