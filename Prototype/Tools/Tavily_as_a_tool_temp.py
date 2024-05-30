
import asyncio

import subprocess
import os

# Tool for communicating to separate virtual env
# Is required as ResearchGPT runs on different version of langchain
# Which has conflicting dependencies with the other version

import asyncio
import subprocess

async def run_python_script_in_environment(venv_activate_path, python_file_path, input_question):
    try:
        # Activate the virtual environment and run the Python script within it
        process = await asyncio.create_subprocess_exec(
            f"{venv_activate_path}/bin/python3.11", python_file_path, input_question,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        # Capture and return the output of the Python script
        if stderr:
            print(f"Error running Python script in virtual environment: {stderr.decode()}")
            return None
        return stdout.decode().strip()

    except Exception as e:
        print(f"Error running Python script in virtual environment: {e}")
        return None

async def call_other_environment(venv_activate_path, python_file_path, input_question):
    try:
        report = await run_python_script_in_environment(
            venv_activate_path, python_file_path, input_question
        )
        if report is None:
            return None

        # Removing subparts of report
        # index_intro = report.find("## Table of Contents")
        # if index_intro != -1:
        #     report = report[index_intro:]

        if True:
            file_path = "/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Prototype/detailed_report_storage.txt"

            with open(file_path, "r") as file:
                text = file.read()
            report = text

        return report

    except Exception as e:
        print(f"Error: {e}")
        return None


def ResearchGPT(input: str) -> str:
    """
    This is a sample script that shows how to run a research report.
    """

    # Normal tool execution

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
    input = "What are the audit risks in the order to cash process in Consumer Goods sector (at Procter & Gamble)? Please try to be as specific as you can!"
    report = ResearchGPT(input)
    print(report)
