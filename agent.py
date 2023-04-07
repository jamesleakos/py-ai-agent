# load .env vars
from dotenv.main import load_dotenv
import os
load_dotenv()

# set up openai
import openai
openai.api_key = os.environ.get('OPENAI_API_KEY')

OBJECTIVE = 'Solve the following riddle: "Five people were eating apples, A finished before B, but behind C. D finished before E, but behind B. What was the finishing order?"'
MAX_LOOPS = 5

def openai_call(prompt, use_4 = True):
    if use_4:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.6,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response.choices[0].text.strip()
    else:
        messages=[{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages = messages,
            temperature=0.6,
            max_tokens=100,
            n=1,
            stop=None,
        )
        return response.choices[0].message.content.strip()


def task_creation_agent_start(objective):
    prompt = f"You are an task creation AI that uses the result of an execution agent to create tasks to achieve the following objective: {objective}. Return the tasks as an array."
    response = openai_call(prompt)
    return response.split('\n')


def task_creation_agent(objective, prev_result, prev_task, task_list):
    prompt = f"You are an task creation AI that uses the result of an execution agent to create new tasks with the following objective: {objective}, The last completed task has the result: {prev_result}. This result was based on this task description: {prev_task}. These are incomplete tasks: {', '.join(task_list)}. Based on the result, create new tasks to be completed by the AI system that do not overlap with incomplete tasks. Return the tasks as an array."
    response = openai_call(prompt)
    return response.split('\n')


def priotization_agent(task_list):
    prompt = f"""You are an task prioritization AI tasked with cleaning the formatting of and reprioritizing the following tasks: {', '.join(task_list)}. Consider the ultimate objective of your team:{OBJECTIVE}. Do not remove any tasks. Return the result as a numbered list, like:
    #. First task
    #. Second task
    """
    response = openai_call(prompt)
    return response.split('\n')

def execution_agent(objective, task):
    prompt =f"You are an AI who performs one task based on the following objective: {objective}.\nYour task: {task}\nResponse:"
    return openai_call(prompt)

def main_loop(task_list):
    prev_result = ''
    prev_task = ''
    for i in range(MAX_LOOPS):
        # some loop info
        print(f'----------LOOP {i}-----------\n\n\n')
        print(f'TASK LIST:', task_list, '\n\n')

        # execute the task list
        task = task_list.pop(0)
        result = execution_agent(OBJECTIVE, task)
        print('RESULT:', result, '\n\n')

        # update the task list
        task_list = task_creation_agent(OBJECTIVE, result, task, task_list)
        print('task_list POST CREATION AGENT:', task_list, '\n\n')
        task_list = priotization_agent(task_list)
        print('task_list POST priotization_agent:', task_list, '\n\n')


task_list = task_creation_agent_start(OBJECTIVE)
main_loop(task_list)
        