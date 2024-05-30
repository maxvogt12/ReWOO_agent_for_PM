# Master-Thesis
Repo for development of a prototype for implementing LLMs into PM4PY. As the practical side of my master thesis for the MSc 'ICT in Business' at Leiden University in 2024. This repo is in active development and contains both working and archived files. So this is not just a working prototype but also a process tracker. This is a private repository, due to the fact that it contains API keys which can be coupled to payment information. 

## Concept
Researching if LLMs can supplement domain knowledge (about the sector, organization, process, etc.) into process mining tools and whether this offers additional value compared to the current status of these tools. The system is a multi-level agent, based on GPT-4 Turbo and GPT-3.5 Turbo.

### Input
1. event log
2. name of the organisation
3. type of process

### Output
1. generated process model (BPMN, Petri net, Heuristic net, etc.)
2. found relevant process components
3. potential explanations/ causes for issues at these components
4. potential remediations for these issues
5. the generated graph of the used agent

## Programming languages
Main language is Python.

## (Current) Architecture prototype
### Flow
![image](https://github.com/maxvogt12/Master-Thesis/blob/6cb9fa36bc6024f6cf55135f26848d02905a9927/Prototype/Images/Agent_flow-FlowChart.drawio-4.png)
### Components
![image](https://github.com/maxvogt12/Master-Thesis/blob/5228f09ab57f6aa28fb90b366cf4bebd02e7518d/Prototype/Images/Architecture-New_Components.drawio-4.png)

## Example of input and output
### Example of input
"Can you find the bottlenecks and inefficiencies in process based on the following event log, filepath='file_path' This is an order to cash process at Procter & Gamble (P&G). What are potential causes for the inefficiencies that you identified? Please use the variants approach for process discovery."

### Generated Heuristic net
<img src="https://github.com/maxvogt12/Master-Thesis/blob/42cb89d7c34dcac16fd19d3e5d2acc715cffe010/Prototype/Images/Heuristic_net.png" width= "300">

### Inefficiencies + explanations
<img src="https://github.com/maxvogt12/Master-Thesis/blob/d325bfa2844a5c602e2c60f40a5c8ca63a223f59/Prototype/Images/Example_output.png" width= "1400">

### Agent graph
<img src="https://github.com/maxvogt12/Master-Thesis/blob/818955110b54d87f12afd9d612a6f607db06c4fc/Prototype/Images/state_graph.png" width= "300">

## Main components
### LangChain
LangChain is used as the basis for this prototype, LangChain is a widely used open-source library for building LLM-based applications. For this prototype LangChain is used to build the agent that executes the given tools to generate the mentioned output. 
For more info, see https://www.langchain.com

### Tavily GPT-Researcher
For gathering more complex information from the internet the Tavily GPT-Researcher is used as one of the tools for the agent. This function requires a different version of LangChain compared to some other used functions. Therefore this tool runs in a separate virtual environment, see architecture. This tool generates a research report based on a provided quer and has the following architecture:

<img src="https://github.com/maxvogt12/Master-Thesis/blob/b44ce59f093ecc0177bb521f9f8f4c51ff10c6ca/Prototype/Images/GPT-researcher.png" width= "250">

### REWOO
Reason without observation, is a novel approach for building LLM agents proposed by Xu, et. al. This approach builds on the concepts of ReAct and Plan and Solve prompting and results in more efficient agents that use less tokens and LLM calls. REWOO uses a multi-step planner and variable substitution for effective tool use. It was designed to improve on the ReACT-style agent architecture.

The REWOO paper: https://arxiv.org/abs/2305.18323
The concept of REWOO visualized:
<img src="https://github.com/maxvogt12/Master-Thesis/blob/d69e1918b4109e8469e74c73973fbc1a1770df27/Prototype/Images/REWOO.png" width= "500">

