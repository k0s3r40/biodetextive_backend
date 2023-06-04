
import requests
import json
from django.conf import settings
OPENAI_KEY = settings.OPENAI_KEY

def get_openai_data(messages):
    headers = {'Authorization': f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"}
    request_body = {
        'model': 'gpt-3.5-turbo',
        'messages': messages,
    }
    # return 'Communication error.'
    # return 'Communication error.'
    # models = requests.get('https://api.openai.com/v1/models', headers=headers)
    # print(models.json())
    # print(request_body)
    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', json=request_body, headers=headers)
        response.raise_for_status()  # raise an error if the response status code is not 200
        json_data = response.json()

        # print(response.json())
        choices = json_data.get('choices', [{'message': {'content': 'Communication error.'}}])
        message_content = choices[0].get('message', {}).get('content', 'Communication error.')
        return message_content
    except (requests.exceptions.RequestException, json.JSONDecodeError, TypeError) as e:
        print(f"Failed to get response from OpenAI API: {e}")
        return 'Communication error.'
