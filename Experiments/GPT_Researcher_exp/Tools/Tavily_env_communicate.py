import subprocess
import os
import sys

# Tool for communicating to separate virtual env
# Is required as ResearchGPT runs on different version of langchain
# Which has conflicting dependencies with the other version

import asyncio
import subprocess
from General_Settings import Level_of_detail

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
            sys.exit("Stopped execution, report returned none")
            return None

        # Removing subparts of report
        if Level_of_detail.detailled == False:
            index_intro = report.find("## Introduction")
            if index_intro != -1:
                report = report[index_intro:]

        # Removing subparts of report
        # index_intro = report.find("## Table of Contents")
        # if index_intro != -1:
        #     report = report[index_intro:]

        if Level_of_detail.detailled == True:
            file_path = "/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Prototype/detailed_report_storage.txt"

            with open(file_path, "r") as file:
                text = file.read()
            report = text

        return report

    except Exception as e:
        print(f"Error: {e}")
        return None





# async def activate_virtual_environment(venv_activate_path):
#     try:
#         # Activate the virtual environment
#         activate_cmd = f"source {venv_activate_path}"
#         process = await asyncio.create_subprocess_shell(activate_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         _, _ = await process.communicate()

#     except subprocess.CalledProcessError as e:
#         print(f"Error activating virtual environment: {e}")

# async def run_python_script_in_environment(venv_activate_path, python_file_path, input_question):
#     try:
#         # Get the path to the Python executable within the virtual environment
#         python_executable = os.path.join(os.path.dirname(venv_activate_path), 'python')
        
#         # Run the Python file within the activated virtual environment
#         process = await asyncio.create_subprocess_exec(python_executable, python_file_path, input_question,
#                                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         output, _ = await process.communicate()
#         # Capture the report from the output
#         report = output.decode().strip()
#         return report

#     except subprocess.CalledProcessError as e:
#         print(f"Error running Python script in virtual environment: {e}")
#         return None

# async def call_other_environment(venv_activate_path, python_file_path, input_question):
#     try:
#         await activate_virtual_environment(venv_activate_path)
#         report = await run_python_script_in_environment(venv_activate_path, python_file_path, input_question)

#         # Removing subparts of report
#         index_intro = report.find("## Introduction")
#         if index_intro != -1:
#             report = report[index_intro:]
#         return report

#     except Exception as e:
#         print(f"Error: {e}")
#         return None








