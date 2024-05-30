import pm4py
import pandas as pd

file_path= "/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/flight_event_log.csv"
file_path = "/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/roadtraffic100traces.xes"

# df = pd.read_csv(file_path, sep=',')
# print(df.columns)

event_log = pm4py.read_xes(file_path)
df = pm4py.convert_to_dataframe(event_log)
print(df.columns)

# If required, convert time format
#df['Timestamp'] = pd.to_datetime(df['Timestamp'])

#df = pm4py.format_dataframe(df, case_id='Flight', activity_key='Activity', timestamp_key='Timestamp')

pm4py.view_dotted_chart(df, format='png')
pm4py.view_dotted_chart(df, attributes=['time:timestamp', 'concept:name', 'org:resource'])