import os
from gpt_researcher import GPTResearcher
import asyncio
import sys

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["TAVILY_API_KEY"] = os.getenv('TAVILY_API_KEY')

async def get_report(query: str, report_type: str) -> str:
    researcher = GPTResearcher(query, report_type)
    report = await researcher.run()
    return report

async def main():
    # Access the input_question argument passed from the subprocess function
    if len(sys.argv) > 1:
        input_query = sys.argv[1]
    else:
        print("No input question provided.")
        input_query = None

    query = input_query
    report_type = "research_report"

    report = await get_report(query, report_type)
    return(report)

if __name__ == "__main__":
    asyncio.run(main())

