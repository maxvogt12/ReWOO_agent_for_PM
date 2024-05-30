from langchain_openai import ChatOpenAI
import langchain
import os
from dotenv import load_dotenv
from Tools.Tavily_as_a_tool import ResearchGPT


# Load environment variables from .env file
load_dotenv()

# Environmental variables
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')

# Activating LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "True"
os.environ["LANGCHAIN_PROJECT"] = "Deloitte_REWOO_PM_extended"

# Debug setting for more details during generation of output
langchain.debug = True

# Defining agent components
model = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")

# Initializing agent
if __name__ == "__main__":
     # input query
    task1_var_audit_risk = "What are specific audit risks in the order to cash process in Consumer goods sector (at Procter & Gamble)?"

     # Running the agent
    input_query = task1_var_audit_risk

    response = ResearchGPT(input_query)
    print("Final output: \n", response)

    # Writing agent response to file
    file_write = open("GPT_Researcher_output.txt", "w")
    file_write.write(response)
    file_write.close()


