import requests


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
