
import base64
import json
import requests
from django.conf import settings
# Your Cloud Vision API key
api_key = settings.GOOGLE_API_KEY

# Path to your image file
image_path = 'gg.jpeg'

# Read the image file in binary mode
with open(image_path, 'rb') as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

# Prepare the request payload
payload = {
    'requests': [
        {
            'image': {
                'content': encoded_string
            },
            'features': [
                {
                    'type': 'LABEL_DETECTION',
                    'maxResults': 5
                },
            ]
        }
    ]
}

# Prepare headers
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Prepare the request url
url = f'https://vision.googleapis.com/v1/images:annotate?key={api_key}'

# Make the POST request
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Print the response
print(response.json())