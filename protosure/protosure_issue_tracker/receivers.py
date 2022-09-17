from django.dispatch import receiver
from protosure import Signals


@receiver(Signals.sync_issues)
def create_github_issues(sender, owner, repo, **kwargs):
    print(sender, owner,repo)
