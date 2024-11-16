import openai
import os
from dotenv import load_dotenv

load_dotenv()

def get_competitors(industry):
    api_key = os.environ.get('OPENAI_API_KEY')
    client = openai.OpenAI(
    organization='org-rDJcL7q9nR2pzHnxeN1ipwQF',
    project='proj_Wm3JVHDej00hqCWSR2Ri6wVz',
    api_key=api_key
    )


    my_prompt = """
    List the top three mid to large-cap competitors of a new startup in the %s industry space and list one subreddit on which information about all companies is likely to be found
    Output as a list where the first element is a list of strings of the top competitors and the second element is a list containing a string of the one subreddit
    format:
    [[’company1’, ‘company2’, ‘company3’], [’subreddit_name’]]
    """ % industry


    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": my_prompt}
    ]
    )
    print(completion.choices[0].message.content)
    print(type(completion.choices[0].message.content))
    return completion.choices[0].message.content
