from django.dispatch import receiver
from protosure import Signals
from django.conf import settings

from protosure_issue_tracker.services import get_recent_github_issues
from protosure_issue_tracker import utils


@receiver(Signals.sync_issues)
def create_github_issues(sender, owner, repo, **kwargs):
    github_issues_data = get_recent_github_issues(
        sender=sender, url=f"{settings.GITHUB_REPO}/{owner}/{repo}/issues"
    )
    repository_info = utils.get_repo_info_if_exist_or_create_new_info(owner=owner, repo=repo)
    utils.insert_repo_issue_metadata(repository_info=repository_info, github_issues_data=github_issues_data)
