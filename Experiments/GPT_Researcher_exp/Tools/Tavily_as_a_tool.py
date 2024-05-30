from Tools.Tavily_env_communicate import call_other_environment
import asyncio

def ResearchGPT(input: str) -> str:
    """
    This is a sample script that shows how to run a research report.
    """
    # Normal tool executio
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

# if __name__ == "__main__":
#     input = "What are specific audit risks at the 'Prepare Goods for Shipment' step in the order to cash process in E-commerce retail sector (at Amazon)?"
#     report = ResearchGPT(input)
#     print(report)
