import os
from gpt_researcher import GPTResearcher
import asyncio
import sys
from GPT_Researcher_GitHub.Detailed_report import DetailedReport
# from Prototype.Test_reports.detailed_report1 import detailed_report_1
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
dotenv_path = '/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/.env'
load_dotenv(dotenv_path)

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["TAVILY_API_KEY"] = os.getenv('TAVILY_API_KEY')

# Constants
DETAILED_REPORT_FILE = "/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Prototype/detailed_report_storage.txt"


async def fetch_report(query: str, report_type: str) -> str:
    """
    Fetch a research report based on the provided query and report type.
    """
    researcher = GPTResearcher(query=query, report_type=report_type, config_path=None)
    report = await researcher.conduct_research()
    return report

async def generate_research_report():
    """
    This is a sample script that executes an async main function to run a research report.
    """
     # Access the input_question argument passed from the subprocess function
    if len(sys.argv) > 1:
        input_query = sys.argv[1]
    else:
        print("No input question provided.")
        input_query = None
    
    query = input_query
    report_type = "research_report"

    report = await fetch_report(query, report_type)
    return(report)

async def detailed_run(input_query):
    """
    Run detailed report generation asynchronously.
    """
    query = input_query or "Default query"

    # Initialize the researcher
    researcher = DetailedReport(query=query, config_path=None, source_urls=None, websocket=None)
    
    # Conduct research on the given query
    report = await researcher.run()
    return report

async def main():
    detail_level = Level_of_detail.detailled
    if detail_level:
        input_query = sys.argv[1] if len(sys.argv) > 1 else None
        report = await detailed_run(input_query)
        
        # Writing agent response to file
        with open(DETAILED_REPORT_FILE, "w") as file:
            file.write(report)
        
        return report
    else:
        input_query = sys.argv[1] if len(sys.argv) > 1 else None
        report = await generate_research_report(input_query)
        
        # Writing agent response to file
        with open("resource_report.txt", "w") as file:
            file.write(report)
        
        return report


asyncio.run(main())


