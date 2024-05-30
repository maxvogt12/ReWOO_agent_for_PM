import os
import pm4py
import pandas as pd

file_path = "/Users/maxvogt/Downloads/purchase_to_pay_event_log.csv"
dataframe = pd.read_csv(file_path)
dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'])

def conformance_checking():
    midpoint = (len(dataframe))/2 
    midpoint = int(midpoint)
    print(midpoint)

    df_1 = dataframe.iloc[:midpoint,:]
    df_2 = dataframe.iloc[midpoint:,:]
    print("Shape of new dataframes - {} , {}".format(df_1.shape, df_2.shape))

    df1 = pm4py.format_dataframe(df_1, case_id='case_id', activity_key='activity', timestamp_key='timestamp')
    df2 = pm4py.format_dataframe(df_2, case_id='case_id', activity_key='activity', timestamp_key='timestamp')

    log1 = pm4py.convert_to_event_log(df1)
    log2 = pm4py.convert_to_event_log(df2)

    vis = False
    if vis == True:
        process_tree = pm4py.discover_process_tree_inductive(log1)
        bpmn_model = pm4py.convert_to_bpmn(process_tree)
        pm4py.view_bpmn(bpmn_model)

    net, im, fm = pm4py.discover_petri_net_inductive(log1)
    alignments_diagnostics = pm4py.conformance_diagnostics_alignments(log2, net, im, fm)

    print(alignments_diagnostics)


def view_case_duration():
    pm4py.view_case_duration_graph(dataframe, format='png', activity_key='activity', case_id_key='case_id', timestamp_key='timestamp')

def view_event_performance():
    pm4py.view_performance_spectrum(dataframe, ['Act. A', 'Act. C', 'Act. D'], format='png', activity_key='activity', case_id_key='case_id', timestamp_key='timestamp')

if __name__ == "__main__":
    view_event_performance()