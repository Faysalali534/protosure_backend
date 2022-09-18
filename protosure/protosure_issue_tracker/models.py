from django.db import models

# Create your models here.
from django.db.models import Q
from django.forms import URLField


class RepositoryInfoCustomManager(models.Manager):
    def get_existing_info_for_repo_owner(self, owner, repo):
        condition_1 = Q(repository_owner=owner)
        condition_2 = Q(repository_name=repo)
        repository_info = self.filter(condition_1 & condition_2)
        query_result = repository_info[0] if repository_info else None
        return query_result


class RepositoryInfo(models.Model):
    repository_url = URLField(max_length=200)
    repository_name = models.CharField(max_length=100, null=False)
    repository_owner = models.CharField(max_length=100, null=False)

    objects = RepositoryInfoCustomManager()


class IssueMetadataCustomManager(models.Manager):
    def is_metadata_being_repeated(self, issue_number, repository):
        condition_1 = Q(number=issue_number)
        condition_2 = Q(repository=repository)
        query_result = self.filter(condition_1 & condition_2)
        return query_result


class IssueMetadata(models.Model):
    STATES = [
        ('Draft', 'Draft'),
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Merged', 'Merged')

    ]
    number = models.IntegerField()
    title = models.CharField(max_length=250, null=False)
    description = models.TextField(null=True)
    status = models.CharField(max_length=250, choices=STATES, null=False)
    creation_date = models.DateField()
    comment_count = models.IntegerField(default=0)
    comments_url = URLField(max_length=300)
    repository = models.ForeignKey(RepositoryInfo, on_delete=models.CASCADE)
    objects = IssueMetadataCustomManager()


class IssueComments(models.Model):
    issue = models.ForeignKey(RepositoryInfo, on_delete=models.CASCADE)
    comment = models.TextField(null=True, default=None)
