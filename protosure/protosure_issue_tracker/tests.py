from unittest.mock import patch

from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APIClient

# Create your tests here.
from protosure_issue_tracker.models import IssueComments


class GithubSuccessScenarioTestCase(TestCase):
    DOJO_PLATFORM_USERS_INSTANCE = None
    client = APIClient()
    ACCESS_TOKEN = ''
    User = None
    mock_data = {
        'get_comment_data': {"id": 1250318846},
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
        GithubSuccessScenarioTestCase.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + 'ghp_awwNOmIgcj87H1Yc21r1hO8oNzOhtC4eypSF')

    @patch('protosure_issue_tracker.services.requests.get')
    def test_issues_fetch_feature(self, mock_get):
        mock_get.return_value.ok = True

        mock_get.return_value.json.return_value = self.mock_data['get_latest_issues']
        api_url = reverse('all_issues', kwargs={'owner': 'Faysalali534', 'repo': "Backend-Task"})

        response = GithubSuccessScenarioTestCase.client.get(path=api_url, format='json')
        assert response.status_code == 200
        assert response.data

    @patch('protosure_issue_tracker.services.requests.post')
    @patch('protosure_issue_tracker.services.requests.get')
    def test_add_comment(self, mock_get, mock_post):
        mock_get.return_value.ok = True
        mock_post.return_value.ok = True
        mock_get.return_value.json.return_value = self.mock_data['get_latest_issues']
        mock_post.return_value.json.return_value = self.mock_data['get_comment_data']
        kwargs_data = {'issue': 1, 'owner': 'Faysalali534', 'repo': "Backend-Task"}
        api_url = reverse('issue_comment', kwargs=kwargs_data)
        data = {"comment": "changing comment for test"}
        response = GithubSuccessScenarioTestCase.client.post(path=api_url, data=data, format='json')
        issue_comments_instance = IssueComments.objects.filter(
            issue__number__exact=kwargs_data["issue"],
            issue__repository__repository_name__exact=kwargs_data["repo"],
            issue__repository__repository_owner__exact=kwargs_data["owner"],
        )
        assert response.status_code == 201
        assert response.data
        assert issue_comments_instance[0].comment == data['comment']
