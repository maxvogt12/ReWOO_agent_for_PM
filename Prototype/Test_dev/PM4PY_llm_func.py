import pm4py

file_path = "/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/roadtraffic100traces.xes"
file_path = "/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/BPI_Challenge_2013_incidents.xes"

# Variants abstraction
log = pm4py.read_xes(file_path)
variants_abstraction = (pm4py.llm.abstract_variants(log))

# DFG abstraction
dfg_abstraction = pm4py.llm.abstract_dfg(log)

# Event stream abstraction
event_stream_abstraction = pm4py.llm.abstract_event_stream(log)

# Log features abstraction
log_feat_abstraction = pm4py.llm.abstract_log_features(log)

# Case abstraction
case_log = pm4py.read_xes(file_path, return_legacy_log_object=True)
case_abstraction = pm4py.llm.abstract_case(case_log[0])

# Temporal profile
temp_log = pm4py.read_xes(file_path, return_legacy_log_object=True)
temporal_profile = pm4py.discover_temporal_profile(temp_log)
text_abstr = pm4py.llm.abstract_temporal_profile(temporal_profile, include_header=True)

# Log skeleton
log_ske = pm4py.read_xes(file_path, return_legacy_log_object=True)
log_ske = pm4py.discover_log_skeleton(log_ske)
ske_abstraction = pm4py.llm.abstract_log_skeleton(log_ske)

# Declare model
dec_log = pm4py.read_xes(file_path, return_legacy_log_object=True)
dec_log = pm4py.discover_declare(dec_log)
dec_abstraction = pm4py.llm.abstract_declare(dec_log)

print("Variants: \n")
print(variants_abstraction)

print("DFG: \n")
print(dfg_abstraction)


print("Event stream: \n")
print(event_stream_abstraction)


print("Feature: \n")
print(log_feat_abstraction)

print("Case: \n")
print(case_abstraction)

print("Temporal profile: \n")
print(text_abstr)

print("Log skeleton: \n")
print(ske_abstraction)

print("DECLARE model: \n")
print(dec_abstraction)