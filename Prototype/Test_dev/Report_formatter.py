import langchain
from dotenv import load_dotenv
import pm4py
import os

# Load environment variables from .env file
load_dotenv()

def main():
    openai_key = os.getenv('OPENAI_API_KEY')
    #model = "gpt-3.5-turbo"
    model = "gpt-4-turbo"

    # importing unformatted report from txt file
    file_path = "report_tool_output.txt"

    with open(file_path, "r") as file:
        text = file.read()
    unformatted_report = text
   
   # importing separate research reports

    # Building prompt with ICL
    template = """"
    You are a world class report writer, specifically for business processes. 
    You will be given a unformatted research report as input and your task is to create a better and more structured report of this unformatted one. The unformatted report will be the endresult of a process analysis. It will contain 3 process steps or components that were analyzed and for each of those a sub-report was written including separate table of contents and references. You have to combine these 3 subreports into one larger and structured final report.
    You should follow the following steps:
    (1) Write a title for the final report, that has to contain the organization, type of process and sector of the organization (base on the unformatted report).
    (2) Make 1 table of contents, for this you have to combine the original 3 tables of contents into 1. Do not change their order or order of their elements.
    (3) Add all the content sections of the subreports (that come between the table of contents and referenceslist of the subreports) into one. ALL OF THE CONTENT SHOULD BE IN HERE
    (4) Create one references section at the end, by combining the three separate reference sections of the original subreportys. Include all the references of the original report.
    
    Some demands for the final report:
    (1) It needs to have a title
    (2) It needs to have 1 table of contents 
    (3) All of the information of the original 3 table of contents has to be included into the new one. And no additional entries.
    (4) All the information of the original subreports has to be in the final report.
    (5) All information needs references, so include all of the original references. Do not add or remmove any of them!

    It is important to note that your task is just TO RESTRUCTURE! Not to change,add, or remove any information!
    EVERY SINGLE PIECE OF INFORMATION OF THE UNFORMATTED REPORT HAS TO BE IN THE FINAL REPORT OR YOU WILL BE PENALIZED. 
    SO IF THE UNFORMATTED REPORT CONTAINS 10,000 WORDS, THE FINAL REPORT SHOULD ALSO CONTAIN AROUND 10,000 WORDS!

    You will now be given the unformatted report:
    {unformatted_report}

    Begin!
    """
    filled_template = template.format(unformatted_report=unformatted_report)
    prompt = filled_template

    # retrieving reponse from LLM
    resp = pm4py.llm.openai_query(prompt, api_key=openai_key, openai_model=model)

    # Writing agent response to file
    file_write = open("formatted_report.txt", "w")
    file_write.write(resp)
    file_write.close()

    # returning model reponse
    return resp

if __name__ == "__main__":
    print(main())
