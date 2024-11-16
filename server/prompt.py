import json
from generate_sentiment import get_sentiment_context

def prompt(inputs):
    #return example prompt response
    get_sentiment_context(inputs.get('industry'))

    with open('example_response.txt','r') as f:
        json_string = f.read().replace('```json\n', '').replace('\n```', '')
        data = json.loads(json_string)
    return data
