from langchain.tools import BaseTool, StructuredTool, tool
from Tools.Tavily_env_communicate import call_other_environment
import asyncio
import os
from Test_reports.inefficiency_1 import report_ineffficiency_1
from Test_reports.inefficiency_2 import report_ineffficiency_2
from Test_reports.inefficiency_3 import report_ineffficiency_3
from Test_reports.Detailed_reports.Variant.Detailed_report_1 import detailed_report_1
from Test_reports.Detailed_reports.Variant.Detailed_report_2 import detailed_report_2
from Test_reports.Detailed_reports.Variant.Detailed_report_3 import detailed_report_3
from General_Settings import Level_of_detail


@tool
def ResearchGPT(input: str) -> str:
    """
    This is a sample script that shows how to run a research report.
    """

    # Test execution of tool with hardcoded Tavily GPT Researcher reports
    Test = False
    Detail_level = Level_of_detail.detailled
    if Test == True and Detail_level == False:
        report1 = report_ineffficiency_1
        report2 = report_ineffficiency_2
        report3 = report_ineffficiency_3
        if "Validation" in input:
            report = report1
            print("Report 1 used, 27031")
        elif "Credit" in input:
            report = report2
            print("Report 2 used, 27032")
        elif "Shipment" in input:
            report = report3
            print("Report 3 used, 27033")
        else:
            report = ""
            print("Error while selecting test report, 2518GE")
        return report

    # Test execution with detailed reports
    elif Test == True and Detail_level == True:
        report1 = detailed_report_1
        report2 = detailed_report_2
        report3 = detailed_report_3
        if "Credit" in input:
            report = report1
            print("Detailed Report 1 used, 27031")
        elif "Ship" in input:
            report = report2
            print("Detailed Report 2 used, 27032")
        elif "Approval" in input:
            report = report3
            print("Detailed Report 3 used, 27033")
        else:
            report = ""
            print("Error while selecting test report, 2518GE")
        return report

    # Normal tool execution
    else:
        # Setting input args
        old_venv_activate_path = "/Users/maxvogt/Documents/GitHub/Thesis/GPT_Researcher_Venv/bin/activate"
        venv_activate_path = "/Users/maxvogt/Documents/GitHub/Thesis/GPT_Researcher_VirtualEnv"

        old_python_file_path = "/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Prototype/Tools/GPT-researcher.py"
        python_file_path = "/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Prototype/Tools/new_GPT_researcher.py"
        input_question = input

        # Running GPT-researcher in different venv
        report = asyncio.run(call_other_environment(venv_activate_path, python_file_path, input_question))
        # loop = asyncio.new_event_loop()
        # report = loop.run_until_complete(call_other_environment(venv_activate_path, python_file_path, input_question))

    return report

if __name__ == "__main__":
    input = "What are specific audit risks at the 'Prepare Goods for Shipment' step in the order to cash process in E-commerce retail sector (at Amazon)?"
    report = ResearchGPT(input)
    print(report)
