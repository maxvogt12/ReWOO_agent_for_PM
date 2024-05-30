from langchain.tools import BaseTool, StructuredTool, tool
import pm4py
import pandas as pd
import os
from .Visualizer import model_visualizer
from .Analytics_vis import analytics_visualizer
from .CSV_config import CSV_format
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Defining custom tool for PM4PY
@tool
def process_discovery(file_path: str) -> str:
    """Execute process discovery on the provided event log, using the DFG approach"""

    # Distinction between CSV and XES file formats
    if "csv" in file_path:
      # For CSV file formats paramters for 3 columns have to be set manually here
      df = pd.read_csv(file_path, sep=CSV_format.sep)

      # If required, convert time format
      df[CSV_format.timestamp] = pd.to_datetime(df[CSV_format.timestamp])

      df = pm4py.format_dataframe(df, case_id=CSV_format.case, activity_key=CSV_format.activity, timestamp_key=CSV_format.timestamp)
      event_log = pm4py.convert_to_event_log(df)
      file_type = "csv"
    else:
      # Reading the event log directly from XES file
      event_log = pm4py.read_xes(file_path)
      file_type = "xes"

    # Creating DFG abstraction of event log
    abstraction = pm4py.llm.abstract_dfg(event_log)

    # Visualizing process models using the preferred format
    model_visualizer(event_log)

    # Visualizing analytics about the data
    analytics_visualizer(event_log, file_type)

    # Importing user query
    file_path = "agent_input.txt"

    with open(file_path, "r") as file:
        text = file.read()
    original_query = text
   
    openai_key = os.getenv('OPENAI_API_KEY')
    model = "gpt-3.5-turbo"
    # Building prompt with ICL
    template = """"
    You are a world class process consultant, specialized in analyzing processes and the components of processes. You will be tasked to make an analysis on a provided process (for instance on inefficiencies, audit risks, regulatory risks, etc.). From this process you will have to select a top 3 of process steps or components.
    You should list those steps/components of the provided process in a structured way in your response.\n
    Below the processes is displayed using the 'variants' approach. Meaning that all the process variants are listed below with their respective frequency and performance. A process variant is a sequence of process activities with a start event and a final event. 
    You should interpret the provided process data as:
        1. frequency is quantified by the instances where a pair of activities are sequential, and performance is calculated as an aggregation, such as average or median, of recorded times between the two activities. For a process variant, frequency is determined by the count of cases following the given trace. 
        2. Performance is an aggregation, such as average or median, of total throughput times for the cases.
    You should base your analysis on the original user instruction. That contains a analysis type like efficiency or certain type of risks. Based on that type you have tyo conduct an analysis on the process and provide the 3 most relevant process components or steps.
    The user instruction is the following:
    {user_query}

    Can you give me the top 3 process steps/ activities of your analysis? And provide an explanation for each. Just give the top 3 process steps and their explanation, nothing else.
    List those in a strucutured way. Here is the process you have to analyze:\n
    """
    filled_template = template.format(user_query=original_query)
    prompt = filled_template + abstraction
    # retrieving reponse from LLM
    resp = pm4py.llm.openai_query(prompt, api_key=openai_key, openai_model=model)
    return resp
