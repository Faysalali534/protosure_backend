from django.apps import AppConfig


class ProtosureIssueTrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'protosure_issue_tracker'

    def ready(self):
        from protosure_issue_tracker import receivers
