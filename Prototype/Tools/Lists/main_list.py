from urllib import response
from langchain import hub
from langchain.agents import initialize_agent, Tool
from langchain import Wikipedia
import langchain
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.retrievers.tavily_search_api import TavilySearchAPIRetriever
from langchain_community.utilities import BingSearchAPIWrapper
from langchain.tools.bing_search.tool import BingSearchRun
from langchain_exa import ExaSearchRetriever, TextContentsOptions
from langchain.agents import tool
from Tools.Process_Mining.ProcessMining_Tool import process_discovery

from Tools.LLM_as_a_tool import ChatGPT_response
from Tools.Human_as_a_tool import human_tool
from Tools.Tavily_as_a_tool import ResearchGPT
from Tools.Report_tool import Report
from Tools.Process_Mining.Temporal_profile import temporal_profile
from Tools.Process_Mining.Variants_tool import variants
from Tools.Process_Mining.PM_approach_selector import approach_selector


# Separate tools for agent

def ProcessDiscovery_DFG(event_log):
    response = process_discovery(event_log)
    return response

def ProcessResearcher(query):
    response = ResearchGPT(query)
    return response
 
def ChatGPT(query):
    response = ChatGPT_response(query)
    return(response)

def human(query):
    response = human_tool(query)
    return response

def Generate_report(query):
    response = Report(query)
    return response

def ProcessDiscovery_Temporal_Profile(event_log):
    response = temporal_profile(event_log)
    return response

def ProcessDiscovery_Variants(event_log):
    response = variants(event_log)
    return response

def Selector_Process_Discovery(query):
    response = approach_selector(query)
    return response