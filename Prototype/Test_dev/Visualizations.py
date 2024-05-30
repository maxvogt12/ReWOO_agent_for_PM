import pm4py

file_path = "/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/roadtraffic100traces.xes"

event_log = pm4py.read_xes(file_path)
df = pm4py.convert_to_dataframe(event_log)
print(df.head)

# View distribution of events per day of the week
#pm4py.view_events_distribution_graph(df, format='png', distr_type='days_week', activity_key='concept:name', case_id_key='case:concept:name', timestamp_key='time:timestamp')

# View event per time graph
#pm4py.view_events_per_time_graph(df, format='png', activity_key='concept:name', case_id_key='case:concept:name', timestamp_key='time:timestamp')

# View case duration
#pm4py.view_case_duration_graph(df, format='png', activity_key='concept:name', case_id_key='case:concept:name', timestamp_key='time:timestamp')

# View SNA
metric = pm4py.discover_subcontracting_network(df, resource_key='org:resource', timestamp_key='time:timestamp', case_id_key='case:concept:name')
pm4py.view_sna(metric)

# View performance spectrum
#pm4py.view_performance_spectrum(df, ['Act. A', 'Act. C', 'Act. D'], format='png', activity_key='concept:name', case_id_key='case:concept:name', timestamp_key='time:timestamp')