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
                        "maxResults": 50,
                        "type": "LANDMARK_DETECTION"
                    },
                    {
                        "maxResults": 50,
                        "type": "FACE_DETECTION"
                    },
                    {
                        "maxResults": 50,
                        "type": "OBJECT_LOCALIZATION"
                    },
                    {
                        "maxResults": 50,
                        "type": "LOGO_DETECTION"
                    },
                    {
                        "maxResults": 50,
                        "type": "LABEL_DETECTION"
                    },
                    {
                        "maxResults": 50,
                        "model": "builtin/latest",
                        "type": "DOCUMENT_TEXT_DETECTION"
                    },
                    {
                        "maxResults": 50,
                        "type": "SAFE_SEARCH_DETECTION"
                    },
                    {
                        "maxResults": 50,
                        "type": "IMAGE_PROPERTIES"
                    },
                    {
                        "maxResults": 50,
                        "type": "CROP_HINTS"
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
    return get_openai_data([{'role': 'user', 'content': f" Animal Plant Mushroom or landmark give me the name \n{json.dumps(response.json())}"}])

