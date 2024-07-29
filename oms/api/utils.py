from typing import Dict

import requests

def send_post_request(url: str, payload: Dict):
    """Post synchronous http requests"""
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)

    return response
