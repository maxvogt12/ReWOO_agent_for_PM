from termios import ICRNL
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_core.prompts import ChatPromptTemplate
from Prompt_Templates.Report_Template import report_prompt
from Prompt_Templates.Report_Template_detailled import report_prompt_detailed
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from General_Settings import Level_of_detail
import pm4py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()



@tool
def Report2(input: str) -> str:
    """
    This tools generates one central report using separate research reports
    """

    outputparser = StrOutputParser()
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")

    if Level_of_detail.detailled == True:
        prompt = ChatPromptTemplate.from_template(report_prompt_detailed)

        chain = prompt | llm | outputparser

        response = chain.invoke({"inefficiencies_and_reports" : input})
        
        #response = input

    elif Level_of_detail.detailled == False:
        prompt = ChatPromptTemplate.from_template(report_prompt)

        chain = prompt | llm | outputparser

        response = chain.invoke({"inefficiencies_and_reports" : input})

    # Writing agent response to file
    file_write = open("report_tool_output.txt", "w")
    file_write.write(response)
    file_write.close()

    return(response)

@tool
def Report(input: str) -> str:
    """
    This tools generates one central report using separate research reports
    """

    outputparser = StrOutputParser()
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")

    if Level_of_detail.detailled == True:
        model = "gpt-3.5-turbo"
        # Building prompt with ICL
        template = report_prompt_detailed
        # Removing subparts of report
        index_intro = input.find("## Table of Contents")
        if index_intro != -1:
            compressed_input = input[:index_intro]
        else:
            print("## Table of Contents not found in input of Report Function")
        #prompt = template + compressed_input
        # retrieving reponse from LLM
        #resp = pm4py.llm.openai_query(prompt, api_key=os.environ["OPENAI_API_KEY"], openai_model=model)
        # response = resp + "\n \n Process inefficiency reports: \n " + input
        response = input

    elif Level_of_detail.detailled == False:
        prompt = ChatPromptTemplate.from_template(report_prompt)

        chain = prompt | llm | outputparser

        response = chain.invoke({"inefficiencies_and_reports" : input})

    # Writing agent response to file
    file_write = open("report_tool_output.txt", "w")
    file_write.write(response)
    file_write.close()

    return(response)