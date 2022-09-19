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


def update_issue(url, sender, payload={}):
    if payload.get('description'):
        payload['body'] = payload.pop('description')
    if payload.get('status'):
        payload['state'] = payload.pop('status').lower()

    headers = {
        'Authorization': sender
    }

    response = requests.patch(url=url, data=json.dumps(payload), headers=headers)
    if response.ok:
        return response.json()
    if response.status_code == 401:
        raise ExternalServiceError(error_code=401, message=response.json().get('message'))

    else:
        raise ExternalServiceError()
