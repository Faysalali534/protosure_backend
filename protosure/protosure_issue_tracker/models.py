from django.db import models

# Create your models here.
from django.forms import URLField


class RepositoryInfo(models.Model):
    repository_url = URLField(max_length=200)
    repository_name = models.CharField(max_length=100, null=False)
    repository_owner = models.CharField(max_length=100, null=False)


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


class IssueComments(models.Model):
    issue = models.ForeignKey(RepositoryInfo, on_delete=models.CASCADE)
    comment = models.TextField(null=True, default=None)
