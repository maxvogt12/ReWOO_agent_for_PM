from urllib import response
import pm4py
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
import os

# Defining custom tool for PM4PY
@tool
def ChatGPT_response(input: str) -> str:
    """Send prompts to LLM and retrieve answer"""
    # Setting API key and model
    api_key = os.getenv('OPENAI_API_KEY')
    model = "gpt-3.5-turbo"
    # Building prompt
    template = ""
    prompt = template + input
    # retrieving reponse from LLM
    resp = pm4py.llm.openai_query(prompt, api_key=api_key, openai_model=model)
    print("Prompt: \n", prompt)
    print("Response: \n", resp)
    return resp
