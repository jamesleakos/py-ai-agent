# py-ai-agent

Simple AI agent using the Open AI API. 

# how it works

The basic premise is as follows:

The user defines an objective. This objective never changes.

Then, a loop begins. A 'task creation agent' asks gpt for a list of tasks that could be used to accomplish the Objective.
Then, an execution agent send that task to gpt and recieves a result. It then asks for the tasks to be updated, executes the next task, etc.

# next up

Add past context of results to the agents. 
