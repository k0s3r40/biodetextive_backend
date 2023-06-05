import base64
import json
import requests
from django.conf import settings
import json

from specimens.open_api_communication import get_openai_data


def analyze_image_with_cloud_vision(image: str):
    api_key = settings.GOOGLE_API_KEY

    payload = {
        "requests": [
            {
                "features": [
                    {
                        "maxResults": 20,
                        "type": "LANDMARK_DETECTION"
                    },
                    {
                        "maxResults": 50,
                        "type": "LABEL_DETECTION"
                    }
                ],
                "image": {
                    "content": image
                },
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    url = f'https://vision.googleapis.com/v1/images:annotate?key={api_key}'

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.json())
    data = []
    for i in response.json().get('responses'):
        for x in i.get('labelAnnotations', []):
            data.append(x.get('description'))
        for x in i.get('landmarkAnnotations', []):
            data.append(x.get('description'))

    request_body = [
        {"role": "system", "content": 'You are part of image recognition app and you can parse json with labels on the picture. Give title of the picture based on whatever the json gives you.'
                                      'describe what is on the picture'},
        {"role": "user", "content": f"From here {data}. A person took up closeup picture of this he does not know what this is  pick one that is some kind of species or a landmark they are usually on the top and output just the name. Just output one label no need of explanation"}
    ]
    return get_openai_data(request_body)
