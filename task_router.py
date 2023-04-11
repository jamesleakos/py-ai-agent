# load .env vars
import sys
from dotenv.main import load_dotenv
import os
load_dotenv()

# set up openai
import openai
openai.api_key = os.environ.get('OPENAI_API_KEY')

CATEGORIES = ['Make a note', 'Set a reminder', 'None of the above']

def openai_completion(prompt, use_4 = False):
    if not use_4:
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

def categorizer(prompt):
    print('\nThe categories are:', ', '.join(CATEGORIES))
    prompt = f"You are an categorizing AI who receives a prompt and checks if it matches a list of possible categories. Here is a prompt: {prompt}. Here is a list the categories: {', '.join(CATEGORIES)}. What category does this prompt match? Category:"
    response = openai_completion(prompt)
    return response

def responder(prompt):
    prompt = f"Please give a helpful response to this prompt: {prompt}. Response:"
    response = openai_completion(prompt)
    return response

def main(prompt):
    print('\nThe prompt is: ', prompt)

    category = categorizer(prompt)
    # vheck if the result is in the list of categories
    if (category not in CATEGORIES or category == 'None of the above'):
        print('\n\n', responder(prompt), '\n\n')
    else:
      print('\n\nThe resulting category is: ', category, '\n\n')


main(sys.argv[1])
        