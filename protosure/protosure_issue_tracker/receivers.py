from django.db.models import Q
from django.dispatch import receiver
from protosure import Signals
from django.conf import settings
import json
import datetime

from protosure_issue_tracker.models import RepositoryInfo
from protosure_issue_tracker.serializers import IssueMetadataSerializer


@receiver(Signals.sync_issues)
def create_github_issues(sender, owner, repo, **kwargs):
    import requests

    url = f"{settings.GITHUB_REPO}/{owner}/{repo}/issues"

    payload = {}
    headers = {
        'Authorization': sender
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    condition_1 = Q(repository_owner=owner)
    condition_2 = Q(repository_name=repo)
    repository_info = RepositoryInfo.objects.filter(condition_1 & condition_2)
    new_repo_info = repository_info[0] if repository_info else None
    if not repository_info:
        new_repo_info = RepositoryInfo.objects.create(repository_owner=owner, repository_name=repo)
    if response.status_code == 200:
        response_from_github = json.loads(response.text)
        try:
            for data in response_from_github:

                data = dict(
                    number=data['number'],
                    title=data['title'],
                    comments_url=data.get('comments_url'),
                    description=data.get('body'),
                    status=data.get('state').capitalize(),
                    comment_count=data.get('comments'),
                    creation_date=datetime.datetime.strptime(data.get('created_at'), '%Y-%m-%dT%H:%M:%SZ').date(),
                    repository=new_repo_info
                )
                new_repo_info.repository_url = data['comments_url']
                new_repo_info.save()
                issue_metadata_serializer = IssueMetadataSerializer(data=data)
                issue_metadata_serializer.is_valid(raise_exception=True)

                issue_metadata_serializer.save(repository_info=new_repo_info)
        except Exception as e:
            print(e)
