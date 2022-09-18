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
                "repository_url": "https://api.github.com/repos/Faysalali534/Backend-Task",
                "comments_url": "https://api.github.com/repos/Faysalali534/Backend-Task/issues/1/comments",
                "number": 1,
                "title": "Found 1 bug",
                "state": "open",
                "comments": 2,
                "created_at": "2022-09-17T14:18:17Z",
                "body": "casdasccccascascasc\r\ncadascas",
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

    @patch('protosure_issue_tracker.services.requests.post')
    @patch('protosure_issue_tracker.services.requests.get')
    def test_filter_fields(self, mock_get, mock_post):
        mock_get.return_value.ok = True
        mock_post.return_value.ok = True
        mock_get.return_value.json.return_value = self.mock_data['get_latest_issues']
        mock_post.return_value.json.return_value = self.mock_data['get_comment_data']
        kwargs_data = {'issue': 1, 'owner': 'Faysalali534', 'repo': "Backend-Task"}
        api_url = reverse('issue_comment', kwargs=kwargs_data)
        data = {"comment": "changing comment for test"}
        GithubSuccessScenarioTestCase.client.post(path=api_url, data=data, format='json')
        kwargs_data.pop('issue')
        api_url = reverse('filter_data', kwargs=kwargs_data)
        staus_check = f"{api_url}?status=open"
        response = GithubSuccessScenarioTestCase.client.get(path=staus_check, format='json')
        assert response.status_code == 200
        assert response.data[0]['issue']['status'].lower() == 'open'

