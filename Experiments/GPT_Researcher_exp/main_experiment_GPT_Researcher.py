import os
from gpt_researcher import GPTResearcher
import asyncio
from Tools.GPT_Researcher_GitHub.Detailed_report import DetailedReport
# from Prototype.Test_reports.detailed_report1 import detailed_report_1
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = '/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/.env'
load_dotenv(dotenv_path)

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["TAVILY_API_KEY"] = os.getenv('TAVILY_API_KEY')

# Constants
DETAILED_REPORT_FILE = "/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Prototype/detailed_report_storage.txt"

async def detailed_run(input_query):
    """
    Run detailed report generation asynchronously.
    """
    query = input_query or "Default query"

    print("QUERY_MARKER: ", query)

    # Initialize the researcher
    researcher = DetailedReport(query=query, config_path=None, source_urls=None, websocket=None)
    
    # Conduct research on the given query
    report = await researcher.run()
    return report

async def main():
    input_query = "What are specific audit risks in the order to cash process in Consumer goods sector (at Procter & Gamble)?"
    report = await detailed_run(input_query)
    
    # Writing agent response to file
    with open(DETAILED_REPORT_FILE, "w") as file:
        file.write(report)
    
    return report


asyncio.run(main())


