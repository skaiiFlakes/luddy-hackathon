import json

def prompt(inputs):
    #return example prompt response
    with open('server/example_response.txt','r') as f:
        json_string = f.read().replace('```json\n', '').replace('\n```', '')
        data = json.loads(json_string)
    return data
