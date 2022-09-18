from django.db.models.signals import pre_init
from django.dispatch import receiver

from protosure_issue_tracker.models import IssueMetadata
import django.dispatch

sync_issues = django.dispatch.Signal(providing_args=["owner", "repo"])
insert_comments_to_issue = django.dispatch.Signal(providing_args=["owner", "repo", "issue_id"])
