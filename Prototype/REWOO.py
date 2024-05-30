from langchain_openai import ChatOpenAI
import langchain
from Tools.Lists.main_list import ProcessDiscovery_DFG, ProcessResearcher, ChatGPT, human, Generate_report, ProcessDiscovery_Temporal_Profile, ProcessDiscovery_Variants, Selector_Process_Discovery
import os
from Prompt_Templates.REWOO_Template import REWOO_prompt
from Prompt_Templates.REWOO_Template_detail import REWOO_prompt_detail
import re
from langchain_core.prompts import ChatPromptTemplate
from Prompt_Templates.Solver_Template import Solver_prompt
from langgraph.graph import StateGraph, END
import matplotlib.pyplot as plt
from Graph_visualize import graph_visualize_ASCII, graph_visualize_png
from typing import TypedDict, List
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
from General_Settings import Level_of_detail

# Load environment variables from .env file
load_dotenv()

# Environmental variables
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')

# Activating LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "True"
os.environ["LANGCHAIN_PROJECT"] = "Deloitte_REWOO_PM_extended"

# Debug setting for more details during generation of output
langchain.debug = True

# Defining agent components
model = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")

class ReWOO(TypedDict):
    task: str
    plan_string: str
    steps: List
    results: dict
    result: str

# Regex to match expressions of the form E#... = ...[...]
regex_pattern = r"Plan:\s*(.+)\s*(#E\d+)\s*=\s*(\w+)\s*\[([^\]]+)\]"
if Level_of_detail.detailled == True:
    prompt_template = ChatPromptTemplate.from_messages([("user", REWOO_prompt_detail)])
else:
    prompt_template = ChatPromptTemplate.from_messages([("user", REWOO_prompt)])
planner = prompt_template | model

# Importing REWOO prompt
REWOO_prompt = REWOO_prompt

def get_plan(state: ReWOO):
    task = state["task"]
    result = planner.invoke({"task": task})
    # Find all matches in the sample text
    matches = re.findall(regex_pattern, result.content)
    return {"steps": matches, "plan_string": result.content}

def _route(state):
    _step = _get_current_task(state)
    if _step is None:
        # We have executed all tasks
        return "solve"
    else:
        # We are still executing tasks, loop back to the "tool" node
        return "tool"

def _get_current_task(state: ReWOO):
    if state["results"] is None:
        return 1
    if len(state["results"]) == len(state["steps"]):
        return None
    else:
        return len(state["results"]) + 1


def tool_execution(state: ReWOO):
    search = TavilySearchResults()
    """Worker node that executes the tools of a given plan."""
    _step = _get_current_task(state)
    _, step_name, tool, tool_input = state["steps"][_step - 1]
    _results = state["results"] or {}
    for k, v in _results.items():
        tool_input = tool_input.replace(k, v)
    if tool == "Google":
        result = search.invoke(tool_input)
    elif tool == "Generate_report":
        result = Generate_report(tool_input)
    elif tool == "ProcessDiscovery_DFG":
        result = ProcessDiscovery_DFG(tool_input)
    elif tool == "ProcessDiscovery_Temporal_Profile":
        result = ProcessDiscovery_Temporal_Profile(tool_input)
    elif tool == "ProcessDiscovery_Variants":
        result = ProcessDiscovery_Variants(tool_input)
    elif tool == "ProcessResearcher":
        result =  ProcessResearcher(tool_input)
    elif tool == "LLM":
        result = ChatGPT(tool_input)
    elif tool == "Selector_Process_Discovery":
        result = Selector_Process_Discovery(tool_input)
    else:
        raise ValueError
    _results[step_name] = str(result)
    return {"results": _results}

def solve(state: ReWOO):
    plan = ""
    for _plan, step_name, tool, tool_input in state["steps"]:
        _results = state["results"] or {}
        for k, v in _results.items():
            tool_input = tool_input.replace(k, v)
            step_name = step_name.replace(k, v)
        plan += f"Plan: {_plan}\n{step_name} = {tool}[{tool_input}]"
    prompt = Solver_prompt.format(plan=plan, task=state["task"])
    result = model.invoke(prompt)
    return {"result": result.content}

def main_initialize(task):

    # Building the graph
    graph = StateGraph(ReWOO)
    graph.add_node("plan", get_plan)
    graph.add_node("tool", tool_execution)
    graph.add_node("solve", solve)
    graph.add_edge("plan", "tool")
    graph.add_edge("solve", END)
    graph.add_conditional_edges("tool", _route)
    graph.set_entry_point("plan")

    app = graph.compile()

    for s in app.stream({"task": task}):
        print(s)
        print("---")

    # Print out the final result
    response = (s[END]["result"])

    # Visualzing the generated graph
    graph_visualize_png(app)
    graph_visualize_ASCII(app)

    return response


# Initializing agent
if __name__ == "__main__":

    # task 1 (P&G case) has hardcoded research reports in the "Test_reports" folder
    # required class settings: sep = ';', Case id, Activity name, Timestamp
    task1_TP = "Can you find the bottlenecks and inefficiencies in process based on the following event log, filepath=/Users/maxvogt/Downloads/Event logs/order_to_cash_event_log_05012023.csv? This is an order to cash process at Procter & Gamble (P&G). What are potential causes for the inefficiencies that you identified? Please use the temporal profile approach for process discovery."
    task1_DFG = "Can you find the bottlenecks and inefficiencies in process based on the following event log, filepath=/Users/maxvogt/Downloads/Event logs/order_to_cash_event_log_05012023.csv? This is an order to cash process at Procter & Gamble (P&G). What are potential causes for the inefficiencies that you identified? Please use the DFG approach for process discovery."
    task1_var = "Can you find the bottlenecks and inefficiencies in process based on the following event log, filepath=/Users/maxvogt/Downloads/Event logs/order_to_cash_event_log_05012023.csv? This is an order to cash process at Procter & Gamble (P&G). What are potential causes for the inefficiencies that you identified? Please use the variants approach for process discovery."

    # required class settings: sep = ',', case_id, activity, timestamp
    task2_DFG = "Can you find the bottlenecks and inefficiencies in process based on the following event log, filepath=/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/purchase_to_pay_event_log.csv? This is an purchase to pay process at IKEA. What are potential causes for the inefficiencies that you identified? Please use the DFG approach for process discovery."
    task2_TP = "Can you find the bottlenecks and inefficiencies in process based on the following event log, filepath=/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/purchase_to_pay_event_log.csv? This is an purchase to pay process at IKEA. What are potential causes for the inefficiencies that you identified? Please use the temporal profile approach for process discovery."
    task2_var = "Can you find the bottlenecks and inefficiencies in process based on the following event log, filepath=/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/purchase_to_pay_event_log.csv? This is an purchase to pay process at IKEA. What are potential causes for the inefficiencies that you identified? Please use the variants approach for process discovery."

    # Queries for other perspectives than inefficiencies
    task2_var_audit_risk = "Can you find the audit risks in the process based on the following event log, filepath=/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/purchase_to_pay_event_log.csv? This is an purchase to pay process at IKEA. What are the audit risks for specific steps that you identified? Please use the variants approach for process discovery."
    task2_var_sustainability_risk = "Can you find the sustainability risks in the process based on the following event log, filepath=/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/purchase_to_pay_event_log.csv? This is an purchase to pay process at IKEA. What are the sustainability risks for specific steps that you identified? Please use the variants approach for process discovery."
    task2_TP_cyber_risk = "Can you find the cyber security risks in the process based on the following event log, filepath=/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/purchase_to_pay_event_log.csv? This is an purchase to pay process at IKEA. What are the cyber security risks for specific steps that you identified? Please use the temporal profile approach for process discovery."
    task2_TP_financial_risk = "Can you find the financial risks in the process based on the following event log, filepath=/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/purchase_to_pay_event_log.csv? This is an purchase to pay process at IKEA. What are the financial risks for specific steps that you identified? Please use the temporal profile approach for process discovery."

    # For P&G
    task1_var_audit_risk = "Can you find the causes for audit risks in process based on the following event log, filepath=/Users/maxvogt/Downloads/Event logs/order_to_cash_event_log_05012023.csv? This is an order to cash process at Procter & Gamble (P&G). What are the audit risks for specific steps that you identified? Please use the variants approach for process discovery."

    # For Amazon
    task1_var_audit_risk_Amazon = "Can you find the causes for audit risks in process based on the following event log, filepath=/Users/maxvogt/Downloads/Event logs/order_to_cash_event_log_05012023.csv? This is an order to cash process at Amazon. What are the audit risks for specific steps that you identified? Please use the variants approach for process discovery."

    # Amazon example without specified PM approach
    task1_audit_risk_NA = "Can you find the causes for audit risks in process based on the following event log, filepath=/Users/maxvogt/Downloads/Event logs/order_to_cash_event_log_05012023.csv? This is an order to cash process at Amazon. What are the audit risks for specific steps that you identified?"
    task1_inefficiency_NA = "Can you find the bottlenecks and inefficiencies in process based on the following event log, filepath=/Users/maxvogt/Downloads/Event logs/order_to_cash_event_log_05012023.csv? This is an order to cash process at Procter & Gamble (P&G). What are potential causes for the inefficiencies that you identified?"
    task2_TP_cyber_NA = "Can you find the cyber security risks in the process based on the following event log, filepath=/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/purchase_to_pay_event_log.csv? This is an purchase to pay process at IKEA. What are the cyber security risks for specific steps that you identified?"

    # Paper experiment query
    # nr 1 - Audit (P&G)
    exp_DFG_audit = "Can you find the audit risks in the process based on the following event log, filepath=/Users/maxvogt/Downloads/Event logs/order_to_cash_event_log_05012023.csv? This is an order to cash process at Procter & Gamble (P&G). What are the audit risks for specific steps that you identified? Please use the DFG approach for process discovery."
    # nr 2 - Regulatory (Wells Fargo)
    exp_TP_regulatory = "Can you find the regulatory risks in the process based on the following event log, filepath=/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/LoanApplication.xes? This is a loan application process at Wells Fargo bank. What are the regulatory risks for specific steps that you identified? Please use the temporal profile approach for process discovery."
        # nr 2 - variants approach
    exp_TP_regulatory_var = "Can you find the regulatory risks in the process based on the following event log, filepath=/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/LoanApplication.xes? This is a loan application process at Wells Fargo bank. What are the regulatory risks for specific steps that you identified? Please use the variants approach for process discovery."
    # nr 3 - Environmental 
    exp_DFG_enviornmental = "Can you find the environmental and sustainability risks in the process based on the following event log, filepath=/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/purchase_to_pay_event_log.csv? This is an purchase to pay process at Walmart. What are the environmental and sustainability risks for specific steps that you identified? Please use the DFG approach for process discovery."
    # nr 4 - inefficiencies (Volvo):
    exp_DFG_inefficiencies = "Find the bottlenecks and inefficiencies in process based on the folowing event log, filepath/Users/maxvogt/Documents/GitHub/Thesis/Event Logs/BPI_Challenge_2013_incidents.xes? This is the process of handling IT incidents at Volvo. provide common causes and remediations for the inefficiencies in this process."

    # Running the agent
    agent_input_query = exp_DFG_inefficiencies

    # Writing agent input to file
    file_write = open("agent_input.txt", "w")
    file_write.write(agent_input_query)
    file_write.close()
    
    agent_response = main_initialize(agent_input_query)
    print("Final output: \n", agent_response)

    # Writing agent response to file
    file_write = open("output_agent.txt", "w")
    file_write.write(agent_response)
    file_write.close()


