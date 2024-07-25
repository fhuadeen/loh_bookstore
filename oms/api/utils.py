import requests

def send_post_request(url, payload):
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)

    return response
