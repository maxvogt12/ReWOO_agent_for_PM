from langchain.tools import BaseTool, StructuredTool, tool
import pm4py
import pandas as pd
from .CSV_config import CSV_format
from dotenv import load_dotenv
import os
import pm4py

# Load environment variables from .env file
load_dotenv()

# Defining custom tool for PM4PY
@tool
def approach_selector(user_query: str) -> str:
    """This tool selects which process mining/ discovery approach should be used if the user did not specify a preference"""

    openai_key = os.getenv('OPENAI_API_KEY')


    # Reading approach mapping document
    file_path = "/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Prototype/Tools/Process_Mining/PM_approach_mapping.txt"
    with open(file_path, "r") as file:
        text = file.read()
    mapping = text


    model = "gpt-3.5-turbo"
    # Building prompt with ICL
    template = """"
    You are a world class process mining expert. Your task is to determine the best process mining approach based on the type of analysis that the user wants to execute. There are 3 options for the process mining approaches: (1) DFG, (2) Temporal Profile, (3) Variants.
    The type of analysis could be any type that the user wants, examples are: inefficiencies, bottlenecks, audit risks, cyber security risks, regulatory compliance, etc.
    The user query contains the type of analysis that the user wants to execute, please spot is. The user query is:
    {user_query}

    Based on the analysis that you retrieved from the user query, can you propose which process mining approach we should use. Please give a concise answer, I just want to know which approach to use. Base your answer on the following information (if no relevant information is available, use the DFG approach):

    {mapping}

    It is important to note that if the (exact) type of analysis is not mentioned in the provided in the information, you should propose the DFG approach!!! You should only respond with the chosen approach and nothing else! So you have 3 potential responses: (1) DFG, (2) Temporal Profile, (3) Variants
    """
    filled_template = template.format(user_query=user_query, mapping=mapping)
    prompt = filled_template

    # retrieving reponse from LLM
    resp = pm4py.llm.openai_query(prompt, api_key=openai_key, openai_model=model)
    approach = resp

    print("CHOSEN APPROACH: ", approach)
    return approach