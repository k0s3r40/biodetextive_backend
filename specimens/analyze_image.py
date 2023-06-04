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
    return get_openai_data([{'role': 'user', 'content': f"Give me a simple answer only name preferably specie or landmark object of what is on that picture:\n{json.dumps(response.json())}"
                                                         f" If there is slight possibility if specie give me the specie and dont sound like an ai be sertain. Make it like a title."
                                                         f"If is an animal or plant give the breed or the name off the plant and people should not know you are an ai"}])

