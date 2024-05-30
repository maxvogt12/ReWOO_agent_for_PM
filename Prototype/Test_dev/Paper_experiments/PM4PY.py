import pm4py
import pandas as pd
import os
import sys
from dotenv import load_dotenv
sys.path.append('/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Prototype/Tools/Process_Mining/')
from CSV_config import CSV_format

# Load environment variables from .env file
load_dotenv()

# Defining custom tool for PM4PY
def main(input: str) -> str:
    file_path = "/Users/maxvogt/Downloads/Event logs/order_to_cash_event_log_05012023.csv"
    # Distinction between CSV and XES file formats
    if "csv" in file_path:
      # For CSV file formats paramters for 3 columns have to be set manually here
      df = pd.read_csv(file_path, sep=CSV_format.sep)

      # If required, convert time format
      df[CSV_format.timestamp] = pd.to_datetime(df[CSV_format.timestamp])

      df = pm4py.format_dataframe(df, case_id=CSV_format.case, activity_key=CSV_format.activity, timestamp_key=CSV_format.timestamp)
      event_log = pm4py.convert_to_event_log(df)
      file_type = "csv"
    else:
      # Reading the event log directly from XES file
      event_log = pm4py.read_xes(file_path)
      file_type = "xes"

    # Creating DFG abstraction of event log
    abstraction = pm4py.llm.abstract_dfg(event_log)
   
    openai_key = os.getenv('OPENAI_API_KEY')
    model = "gpt-3.5-turbo"

    prompt = input + abstraction
    print(prompt)
    # retrieving reponse from LLM
    resp = pm4py.llm.openai_query(prompt, api_key=openai_key, openai_model=model)
    return resp

if __name__ == "__main__":
    input = "Can you find the audit risks in my process? And give me causes for why they might be happening? The process is an order-to-cash process at Procter and Gamble. I will now give you the DFG abstraction of the process: \n"
    resp = main(input)

    print(resp)

    # Writing agent response to file
    file_write = open("PM4PY_output.txt", "w")
    file_write.write(resp)
    file_write.close()