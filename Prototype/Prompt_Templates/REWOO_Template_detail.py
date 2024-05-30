REWOO_prompt_detail = """For the following task, make plans that can solve the problem step by step. For each plan, indicate \
which external tool together with tool input to retrieve evidence. You can store the evidence into a \
variable #E that can be called by later tools. (Plan, #E1, Plan, #E2, Plan, ...)

Tools can be one of the following:
(1) ProcessDiscovery_DFG[input]: This is a tool that you can use when you have to discover process from an event log. Only use this tool when you need to use the DFG (Directly-Follows Graph) approach.
This tool takes an event log as input and returns the top 3 inefficiencies and bottlenecks with some additional information as output. 
For this tool give the correct input, which is only a file path without any additional data or formatting
(2) ProcessDiscovery_Temporal_Profile[input]: This is a tool that you can use when you have to discover process from an event log. Only use this tool when you need to use the temporal profile approach.
This tool takes an event log as input and returns the top 3 inefficiencies and bottlenecks with some additional information as output. 
For this tool give the correct input, which is only a file path without any additional data or formatting
(3) ProcessDiscovery_Variants[input]: This is a tool that you can use when you have to discover process from an event log. Only use this tool when you need to use the variants approach.
This tool takes an event log as input and returns the top 3 inefficiencies and bottlenecks with some additional information as output. 
For this tool give the correct input, which is only a file path without any additional data or formatting. NOTE: that this tool returns process components instead of steps, use these components for the rest of the plan
(4) ProcessResearcher[input]: This tool has to be used to answer complex questions regarding the process components that were discoverd during process discovery (tool 1,2, and 3).
This tool activates an agent that can create research reports for process and bottlenecks related questions. If you use this tool, include the organization, the process step, and sector of the process. This tools needs a research question as input, look at the original task for that research question topic (like inefficiencies, audit risks, sustainability, etc.)
(5) Generate_report[input]: This tool can generate the research report for the task.
(6) human[input]: useful when all other tools fail and you need input from the human user.
(7) LLM[input]: A pretrained LLM like yourself. Useful when you need to act with general
(8) Selector_Process_Discovery: You have to use this tool if the prefered process mining approach (DFG, Temporal Profile, or Variants) has not been specified by the user in the initial prompt. This tool will then select which approach you have to use. So if the user has not specified a prefernce use this tool! Before you user one of the process discovery tools (tool 1,2, and 3)!
world knowledge and common sense. Prioritize it when you are confident in solving the problem
yourself. Input can be any instruction.

For example:
Task: Find the bottlenecks and inefficiencies in process based on the folowing event log, filepath=/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Event_Logs/BPI_Challenge_2013_incidents.xes. This is the process of managing IT incidents at Volvo, provide common causes for the inefficiencies in this process. Please use the DFG approach.
Plan: Create a process model and find the top 3 inefficiencies #E1 = ProcessDiscovery_DFG[/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Event_Logs/BPI_Challenge_2013_incidents.xes] 
Plan: The previous step provided 3 inefficiencies, I need to capture those in separate evidence variables. For the first one: #E2 = LLM[ What is the first found process inefficiency in the following structured list. Only state the two components of the process step in your answer, like: 'Created -> Finished'. Do not say anything else! The message: \n #E2 ]
Plan: The previous step provided 3 inefficiencies, I need to capture those in separate evidence variables. For the second one: #E3 = LLM[ What is the second found process inefficiency in the following structured list. Only state the two components of the process step in your answer, like: 'Created -> Finished'. Do not say anything else! The message: \n #E2 ]
Plan: The previous step provided 3 inefficiencies, I need to capture those in separate evidence variables. For the third one: #E4 = LLM[ What is the third found process inefficiency in the following structured list. Only state the two components of the process step in your answer, like: 'Created -> Finished'. Do not say anything else! The message: \n #E2 ]
Plan: Search for the sector of the organization. #E5 = LLM[What is the sector of Volvo? Limit your answer to a maximum of three words!]
Plan: Search for common causes for the first process step found (by ProcessDiscovery_DFG) process inefficiency #E6 = ProcessResearcher[What are common causes for process inefficiencies at the '#E2' step in the IT incidents managing process in #E5 sector (at Volvo)?]
Plan: Search for common causes for the second process step found (by ProcessDiscovery_DFG) process inefficiency #E7 = ProcessResearcher[What are common causes for process inefficiencies at the '#E3' step in the IT incidents managing process in #E5 sector (at Volvo)?]
Plan: Search for common causes for the third process step found (by ProcessDiscovery_DFG) process inefficiency #E8 = ProcessResearcher[What are common causes for process inefficiencies at the '#E4' step in the IT incidents managing process in #E5 sector (at Volvo)?]
Plan: Generate a report using the output of the ProcessResearcher runs. #E9 = Generate_report[
   Organization and process: Process of managing IT incidents at Volvo \n
   Found inefficiencies: \n #E1 \n
   #################### First inefficiency and report: #################### \n Process component: (#E2) \n \n \n #E6 \n 
   #################### Second inefficiency and report: #################### \n Process component: (#E3) \n \n \n #E7 \n 
   #################### Third inefficiency and report: #################### \n Process component: (#E4) \n \n \n #E8 \n]
End: Return #E9 without changing it to the user.

Another example (temporal profile):
Task: Find the bottlenecks and inefficiencies in process based on the folowing event log, filepath=/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Event_Logs/BPI_Challenge_2012.xes. This is the manufacturing process at Siemens, provide common causes for the inefficiencies in this process. Please use the Temporal profile approach.
Plan: Create a process model and find the top 3 inefficiencies #E1 = ProcessDiscovery_Temporal_Profile[/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Event_Logs/BPI_Challenge_2012.xes] 
Plan: The previous step provided 3 inefficiencies, I need to capture those in separate evidence variables. For the first one: #E2 = LLM[ What is the first found process inefficiency in the following structured list. Only state the two components of the process step in your answer, like: 'Created -> Finished'. Do not say anything else! The message: \n #E2 ]
Plan: The previous step provided 3 inefficiencies, I need to capture those in separate evidence variables. For the second one: #E3 = LLM[ What is the second found process inefficiency in the following structured list. Only state the two components of the process step in your answer, like: 'Created -> Finished'. Do not say anything else! The message: \n #E2 ]
Plan: The previous step provided 3 inefficiencies, I need to capture those in separate evidence variables. For the third one: #E4 = LLM[ What is the third found process inefficiency in the following structured list. Only state the two components of the process step in your answer, like: 'Created -> Finished'. Do not say anything else! The message: \n #E2 ]
Plan: Search for the sector of the organization. #E5 = LLM[What is the sector of Siemens? Limit your answer to a maximum of three words!]
Plan: Search for common causes for the first process step found (by ProcessDiscovery_Temporal_Profile) process inefficiency #E6 = ProcessResearcher[What are common causes for process inefficiencies at the '#E2' step in the manufacturing process in #E5 sector (at Siemens)?]
Plan: Search for common causes for the second process step found (by ProcessDiscovery_Temporal_Profile) process inefficiency #E7 = ProcessResearcher[What are common causes for process inefficiencies at the '#E3' step in the manufacturing process in #E5 sector (at Siemens)?]
Plan: Search for common causes for the third process step found (by ProcessDiscovery_Temporal_Profile) process inefficiency #E8 = ProcessResearcher[What are common causes for process inefficiencies at the '#E4' step in the manufacturing process in #E5 sector (at Siemens)?]
Plan: Generate a report using the output of the ProcessResearcher runs. #E9 = Generate_report[
   Organization and process: Manufacturing process at Siemens \n
   Found inefficiencies: \n #E1 \n
   #################### First inefficiency and report: #################### \n Process component: (#E2) \n \n \n #E6 \n 
   #################### Second inefficiency and report: #################### \n Process component: (#E3) \n \n \n #E7 \n 
   #################### Third inefficiency and report: #################### \n Process component: (#E4) \n \n \n #E8 \n]
End: Return #E9 without changing it to the user.

Another example (variants):
Task: Find the bottlenecks and inefficiencies in process based on the folowing event log, filepath=/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Event_Logs/BPI_Challenge_2011.xes. This is the patient registration process at St Jude Hospital, provide common causes for the inefficiencies in this process. Please use the Variants approach.
Plan: Create a process model and find the top 3 inefficiencies #E1 = ProcessDiscovery_Temporal_Profile[/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Event_Logs/BPI_Challenge_2011.xes] 
Plan: The previous step provided 3 inefficiencies, I need to capture those in separate evidence variables. For the first one: #E2 = LLM[ What is the first found process inefficiency in the following structured list. Only state the one component of the process in your answer, like: 'Patient Registered'. Do not say anything else! The message: \n #E2 ]
Plan: The previous step provided 3 inefficiencies, I need to capture those in separate evidence variables. For the second one: #E3 = LLM[ What is the second found process inefficiency in the following structured list. Only state the one component of the process in your answer, like: 'Patient Registered'. Do not say anything else! The message: \n #E2 ]
Plan: The previous step provided 3 inefficiencies, I need to capture those in separate evidence variables. For the third one: #E4 = LLM[ What is the third found process inefficiency in the following structured list. Only state the one component of the process in your answer, like: 'Patient Registered'. Do not say anything else! The message: \n #E2 ]
Plan: Search for the sector of the organization. #E5 = LLM[What is the sector of St Jude Hospital? Limit your answer to a maximum of three words!]
Plan: Search for common causes for the first process step found (by ProcessDiscovery_Temporal_Profile) process inefficiency #E6 = ProcessResearcher[What are common causes for process inefficiencies at the '#E2' step in the patient registration process in #E5 sector (at St Jude Hospital)?]
Plan: Search for common causes for the second process step found (by ProcessDiscovery_Temporal_Profile) process inefficiency #E7 = ProcessResearcher[What are common causes for process inefficiencies at the '#E3' step in the patient registration process in #E5 sector (at St Jude Hospital)?]
Plan: Search for common causes for the third process step found (by ProcessDiscovery_Temporal_Profile) process inefficiency #E8 = ProcessResearcher[What are common causes for process inefficiencies at the '#E4' step in the patient registration process in #E5 sector (at St Jude Hospital)?]
Plan: Generate a report using the output of the ProcessResearcher runs. #E9 = Generate_report[
   Organization and process: Patient registration process at St Jude Hospital
   Found inefficiencies: \n #E1 \n
   #################### First inefficiency and report: #################### \n Process component: (#E2) \n \n \n #E6 \n 
   #################### Second inefficiency and report: #################### \n Process component: (#E3) \n \n \n #E7 \n 
   #################### Third inefficiency and report: #################### \n Process component: (#E4) \n \n \n #E8 \n]
End: Return #E9 without changing it to the user.

For example:
Task: What are the audit risks in the process based on the folowing event log, filepath=/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Event_Logs/BPI_Challenge_2013_incidents.xes. This is the process of managing IT incidents at Volvo, provide specific audit risks for the most 'risky' process steps. Please use the DFG approach.
Plan: Create a process model and find the top 3 inefficiencies #E1 = ProcessDiscovery_DFG[/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Event_Logs/BPI_Challenge_2013_incidents.xes] 
Plan: The previous step provided 3 process steps, I need to capture those in separate evidence variables. For the first one: #E2 = LLM[ What is the first found process step in the following structured list. Only state the two components of the process step in your answer, like: 'Created -> Finished'. Do not say anything else! The message: \n #E2 ]
Plan: The previous step provided 3 process steps, I need to capture those in separate evidence variables. For the second one: #E3 = LLM[ What is the second found process step in the following structured list. Only state the two components of the process step in your answer, like: 'Created -> Finished'. Do not say anything else! The message: \n #E2 ]
Plan: The previous step provided 3 process steps, I need to capture those in separate evidence variables. For the third one: #E4 = LLM[ What is the third found process step in the following structured list. Only state the two components of the process step in your answer, like: 'Created -> Finished'. Do not say anything else! The message: \n #E2 ]
Plan: Search for the sector of the organization. #E5 = LLM[What is the sector of Volvo? Limit your answer to a maximum of three words!]
Plan: Search for common causes for the first process step found (by ProcessDiscovery_DFG) process inefficiency #E6 = ProcessResearcher[What are specific audit risks at the '#E2' step in the IT incidents managing process in #E5 sector (at Volvo)?]
Plan: Search for common causes for the second process step found (by ProcessDiscovery_DFG) process inefficiency #E7 = ProcessResearcher[What are specific audit risks at the '#E3' step in the IT incidents managing process in #E5 sector (at Volvo)?]
Plan: Search for common causes for the third process step found (by ProcessDiscovery_DFG) process inefficiency #E8 = ProcessResearcher[What are specific audit risks at the '#E4' step in the IT incidents managing process in #E5 sector (at Volvo)?]
Plan: Generate a report using the output of the ProcessResearcher runs. #E9 = Generate_report[
   Organization and process: Process of managing IT incidents at Volvo \n
   Found audit risks: \n #E1 \n
   #################### First risk report: #################### \n Process component: (#E2) \n \n \n #E6 \n 
   #################### Second risk report: #################### \n Process component: (#E3) \n \n \n #E7 \n 
   #################### Third risk report: #################### \n Process component: (#E4) \n \n \n #E8 \n]
End: Return #E9 without changing it to the user.

You should always just search for one type of analysis (like inefficiencies, cyber security etc.), not multiple ones! That is why you should always generate exactly 3 research reports (1 analysis applied to the 3 found inefficiencies -> give 3 reports)
Begin! 
Describe your plans with rich details. Each Plan should be followed by only one #E.

For example (without user preference for process discovery approach):
Task: What are the audit risks in the process based on the folowing event log, filepath=/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Event_Logs/BPI_Challenge_2013_incidents.xes. This is the process of managing IT incidents at Volvo, provide specific audit risks for the most 'risky' process steps. 
Plan: First I have to determine which Process Discovery tool I should use, I can use the Selector_Process_Discovery tool, #E0 = Selector_Process_Discovery[What are the audit risks in the process based on the folowing event log, filepath=/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Event_Logs/BPI_Challenge_2013_incidents.xes. This is the process of managing IT incidents at Volvo, provide specific audit risks for the most 'risky' process steps.]
Plan: Based on what instruction I got in #E0, I have to use either the ProcessDiscovery_DFG, ProcessDiscovery_Temporal_Profile, or ProcessDiscovery_Variants tool now. To create a process model and find the top 3 inefficiencies. In this case #E0 said that I have to use the Variants approach so I will use the ProcessDiscovery_Variants tool: #E1 = ProcessDiscovery_Variants[/Users/maxvogt/Documents/GitHub/Thesis/GitHub/Master-Thesis/Event_Logs/BPI_Challenge_2013_incidents.xes] 
Plan: The previous step provided 3 process steps, I need to capture those in separate evidence variables. For the first one: #E2 = LLM[ What is the first found process step in the following structured list. Only state the two components of the process step in your answer, like: 'Created -> Finished'. Do not say anything else! The message: \n #E2 ]
Plan: The previous step provided 3 process steps, I need to capture those in separate evidence variables. For the second one: #E3 = LLM[ What is the second found process step in the following structured list. Only state the two components of the process step in your answer, like: 'Created -> Finished'. Do not say anything else! The message: \n #E2 ]
Plan: The previous step provided 3 process steps, I need to capture those in separate evidence variables. For the third one: #E4 = LLM[ What is the third found process step in the following structured list. Only state the two components of the process step in your answer, like: 'Created -> Finished'. Do not say anything else! The message: \n #E2 ]
Plan: Search for the sector of the organization. #E5 = LLM[What is the sector of Volvo? Limit your answer to a maximum of three words!]
Plan: Search for common causes for the first process step found (by ProcessDiscovery_Variants) process inefficiency #E6 = ProcessResearcher[What are specific audit risks at the '#E2' step in the IT incidents managing process in #E5 sector (at Volvo)?]
Plan: Search for common causes for the second process step found (by ProcessDiscovery_Variants) process inefficiency #E7 = ProcessResearcher[What are specific audit risks at the '#E3' step in the IT incidents managing process in #E5 sector (at Volvo)?]
Plan: Search for common causes for the third process step found (by ProcessDiscovery_Variants) process inefficiency #E8 = ProcessResearcher[What are specific audit risks at the '#E4' step in the IT incidents managing process in #E5 sector (at Volvo)?]
Plan: Generate a report using the output of the ProcessResearcher runs. #E9 = Generate_report[
   Organization and process: Process of managing IT incidents at Volvo \n
   Found audit risks: \n #E1 \n
   #################### First risk report: #################### \n Process component: (#E2) \n \n \n #E6 \n 
   #################### Second risk report: #################### \n Process component: (#E3) \n \n \n #E7 \n 
   #################### Third risk report: #################### \n Process component: (#E4) \n \n \n #E8 \n]
End: Return #E9 without changing it to the user.

You should always just search for one type of analysis (like inefficiencies, cyber security etc.), not multiple ones! That is why you should always generate exactly 3 research reports (1 analysis applied to the 3 found inefficiencies -> give 3 reports)
Begin! 
Describe your plans with rich details. Each Plan should be followed by only one #E.

Task: {task}"""
