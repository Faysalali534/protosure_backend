import datetime

from protosure_issue_tracker.models import RepositoryInfo
from protosure_issue_tracker.serializers import IssueMetadataSerializer


def get_repo_info_if_exist_or_create_new_info(owner, repo):
    repository_info = RepositoryInfo.objects.get_existing_info_for_repo_owner(owner=owner, repo=repo)
    if not repository_info:
        repository_info = RepositoryInfo.objects.create(repository_owner=owner, repository_name=repo)
    return repository_info


def insert_repo_issue_metadata(repository_info, github_issues_data):
    if github_issues_data:
        try:
            response_from_github = github_issues_data
            for data in response_from_github:
                data = dict(
                    number=data["number"],
                    title=data["title"],
                    comments_url=data.get("comments_url"),
                    description=data.get("body"),
                    status=data.get("state").capitalize(),
                    comment_count=data.get("comments"),
                    creation_date=datetime.datetime.strptime(
                        data.get("created_at"), "%Y-%m-%dT%H:%M:%SZ"
                    ).date(),
                    repository=repository_info,
                )
                repository_info.repository_url = data['comments_url']
                repository_info.save()
                issue_metadata_serializer = IssueMetadataSerializer(data=data)
                issue_metadata_serializer.is_valid(raise_exception=True)
                issue_metadata_serializer.save(repository_info=repository_info)
        except Exception as e:
            print(e)
