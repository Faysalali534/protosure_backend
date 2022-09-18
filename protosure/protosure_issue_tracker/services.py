import json

import requests

from protosure.custom_exception import ExternalServiceError


def get_recent_github_issues(url, sender, payload={}):
    payload = payload
    headers = {
        'Authorization': sender
    }

    response = requests.get(url=url, data=payload, headers=headers)
    if response.ok:
        return response.json()
    else:
        return None


def insert_comment_to_issue(url, sender, payload={}):
    payload['body'] = payload.pop('comment')
    headers = {
        'Authorization': sender
    }

    response = requests.post(url=url, data=json.dumps(payload), headers=headers)
    if response.ok:
        return response.json()
    else:
        raise ExternalServiceError()
