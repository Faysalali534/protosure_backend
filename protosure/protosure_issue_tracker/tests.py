from unittest.mock import patch

from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APIClient


# Create your tests here.

class TokenGenerationTestCase(TestCase):
    DOJO_PLATFORM_USERS_INSTANCE = None
    client = APIClient()
    ACCESS_TOKEN = ''
    User = None
    mock_data = {
        'get_latest_issues': [
            {
                "url": "https://api.github.com/repos/Faysalali534/Backend-Task/issues/1",
                "repository_url": "https://api.github.com/repos/Faysalali534/Backend-Task",
                "labels_url": "https://api.github.com/repos/Faysalali534/Backend-Task/issues/1/labels{/name}",
                "comments_url": "https://api.github.com/repos/Faysalali534/Backend-Task/issues/1/comments",
                "events_url": "https://api.github.com/repos/Faysalali534/Backend-Task/issues/1/events",
                "html_url": "https://github.com/Faysalali534/Backend-Task/issues/1",
                "id": 1376785333,
                "node_id": "I_kwDOGWKWos5SEBO1",
                "number": 1,
                "title": "Found 1 bug",
                "user": {
                    "login": "Faysalali534",
                    "id": 29105699,
                    "node_id": "MDQ6VXNlcjI5MTA1Njk5",
                    "avatar_url": "https://avatars.githubusercontent.com/u/29105699?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/Faysalali534",
                    "html_url": "https://github.com/Faysalali534",
                    "followers_url": "https://api.github.com/users/Faysalali534/followers",
                    "following_url": "https://api.github.com/users/Faysalali534/following{/other_user}",
                    "gists_url": "https://api.github.com/users/Faysalali534/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/Faysalali534/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/Faysalali534/subscriptions",
                    "organizations_url": "https://api.github.com/users/Faysalali534/orgs",
                    "repos_url": "https://api.github.com/users/Faysalali534/repos",
                    "events_url": "https://api.github.com/users/Faysalali534/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/Faysalali534/received_events",
                    "type": "User",
                    "site_admin": False
                },
                "labels": [],
                "state": "open",
                "locked": False,
                "assignee": None,
                "assignees": [],
                "milestone": None,
                "comments": 2,
                "created_at": "2022-09-17T14:18:17Z",
                "updated_at": "2022-09-17T14:26:23Z",
                "closed_at": None,
                "author_association": "OWNER",
                "active_lock_reason": None,
                "body": "casdasccccascascasc\r\ncadascas",
                "reactions": {
                    "url": "https://api.github.com/repos/Faysalali534/Backend-Task/issues/1/reactions",
                    "total_count": 0,
                    "+1": 0,
                    "-1": 0,
                    "laugh": 0,
                    "hooray": 0,
                    "confused": 0,
                    "heart": 0,
                    "rocket": 0,
                    "eyes": 0
                },
                "timeline_url": "https://api.github.com/repos/Faysalali534/Backend-Task/issues/1/timeline",
                "performed_via_github_app": None,
                "state_reason": None
            }
        ]
    }

    def setUp(self):
        TokenGenerationTestCase.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + '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')

    @patch('protosure_issue_tracker.services.requests.get')
    def test_issues_fetch_feature(self, mock_get):
        mock_get.return_value.ok = True

        mock_get.return_value.json.return_value = self.mock_data['get_latest_issues']
        api_url = reverse('all_issues', kwargs={'owner': 'Faysalali534', 'repo': "Backend-Task"})

        response = TokenGenerationTestCase.client.get(path=api_url, format='json')
        assert response.status_code == 200
        assert response.data

    def test_add_comment(self):
        api_url = reverse('issue_comment', kwargs={'issue': 1, 'owner': 'Faysalali534', 'repo': "Backend-Task"})
        data = {"comment": "changing comment"}
        response = TokenGenerationTestCase.client.post(path=api_url, data=data, format='json')
        assert response.status_code == 200
        assert response.data
