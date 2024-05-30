from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.agents import create_react_agent
import langchain
from Tools.Lists.main_list import ProcessDiscovery, ProcessResearcher, ChatGPT, human, tools_list
from Prompt_Templates.Main_Template import prompt
import os
from typing import TypedDict, List
from Prompt_Templates.REWOO_Template import REWOO_prompt
import re
from langchain_core.prompts import ChatPromptTemplate
from Prompt_Templates.Solver_Template import Solver_prompt
from langgraph.graph import StateGraph, END
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Tuple, Annotated, TypedDict
from langchain.chains.openai_functions import create_structured_output_runnable
import operator
from langchain.chains.openai_functions import create_openai_fn_runnable
from langgraph.graph import StateGraph, END
import asyncio


# Environmental variables
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["TAVILY_API_KEY"] = os.getenv('TAVILY_API_KEY')
os.environ["BING_SUBSCRIPTION_KEY"] = os.getenv('BING_SUBSCRIPTION_KEY')
os.environ["BING_SEARCH_URL"] = os.getenv('BING_SEARCH_URL')

# Activating LangSmith
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "True"
os.environ["LANGCHAIN_PROJECT"] = "Deloitte_PAE"

# Debug setting for more details during generation of output
langchain.debug = True

# Defining agent components
model = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")

tools = tools_list

class PlanExecute(TypedDict):
    input: str
    plan: List[str]
    past_steps: Annotated[List[Tuple], operator.add]
    response: str

class Plan(BaseModel):
    """Plan to follow in future"""

    steps: List[str] = Field(
        description="different steps to follow, should be in sorted order"
    )

planner_prompt = ChatPromptTemplate.from_template(
    """For the given objective, come up with a simple step by step plan. \
This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.

{objective}"""
)
planner = create_structured_output_runnable(
    Plan, ChatOpenAI(model="gpt-4-turbo-preview", temperature=0), planner_prompt
)


class Response(BaseModel):
    """Response to user."""

    response: str


replanner_prompt = ChatPromptTemplate.from_template(
    """For the given objective, come up with a simple step by step plan. \
This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.

Your objective was this:
{input}

Your original plan was this:
{plan}

You have currently done the follow steps:
{past_steps}

Update your plan accordingly. If no more steps are needed and you can return to the user, then respond with that. Otherwise, fill out the plan. Only add steps to the plan that still NEED to be done. Do not return previously done steps as part of the plan."""
)


replanner = create_openai_fn_runnable(
    [Plan, Response],
    ChatOpenAI(model="gpt-4-turbo-preview", temperature=0),
    replanner_prompt,
)

async def execute_step(state: PlanExecute):
    task = state["plan"][0]
    agent_response = await agent_executor.ainvoke({"input": task, "chat_history": []})
    return {
        "past_steps": (task, agent_response["agent_outcome"].return_values["output"])
    }


async def plan_step(state: PlanExecute):
    plan = await planner.ainvoke({"objective": state["input"]})
    return {"plan": plan.steps}


async def replan_step(state: PlanExecute):
    output = await replanner.ainvoke(state)
    if isinstance(output, Response):
        return {"response": output.response}
    else:
        return {"plan": output.steps}


def should_end(state: PlanExecute):
    if state["response"]:
        return True
    else:
        return False


workflow = StateGraph(PlanExecute)

# Add the plan node
workflow.add_node("planner", plan_step)

# Add the execution step
workflow.add_node("agent", execute_step)

# Add a replan node
workflow.add_node("replan", replan_step)

workflow.set_entry_point("planner")

# From plan we go to agent
workflow.add_edge("planner", "agent")

# From agent, we replan
workflow.add_edge("agent", "replan")

workflow.add_conditional_edges(
    "replan",
    # Next, we pass in the function that will determine which node is called next.
    should_end,
    {
        # If `tools`, then we call the tool node.
        True: END,
        False: "agent",
    },
)

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
app = workflow.compile()

async def run(input):
    config = {"recursion_limit": 50}
    inputs = {"input": input}
    async for event in app.astream(inputs, config=config):
        for k, v in event.items():
            if k != "__end__":
                print(v)

async def main():
    task = "Can you find the bottlenecks and inefficiencies in process based on the folowing event log, filepath=/Users/maxvogt/Downloads/Event logs/order_to_cash_event_log_05012023.csv? This is an order to cash process at Procter & Gamble (P&G). What are potential causes for the inefficiencies that you identified? Base your answers on characteristics of this type of organization and the sector"
    await run(task)

# Call the main function to start the asynchronous execution
asyncio.run(main())