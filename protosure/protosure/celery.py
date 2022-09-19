import os
from celery import Celery, shared_task
from django.apps import apps
from django.conf import settings

from protosure_issue_tracker.services import update_issue

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "protosure.settings")
app = Celery("protosure")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])


@shared_task()
def update_bulk_issue_task(owner, repo, data):
    for data_for_req in data.get('data'):
        update_issue(
            sender=data['sender'], url=f"{settings.GITHUB_REPO}/{owner}/{repo}/issues/{data_for_req['issue_number']}",
            payload=dict(status=data_for_req["status"]
                         ))
