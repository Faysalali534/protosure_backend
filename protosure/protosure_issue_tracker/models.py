import datetime

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

    def does_issue_number_exist(self, issue_number, repository, owner):
        condition_1 = Q(number__exact=issue_number)
        condition_2 = Q(repository__repository_name__exact=repository)
        condition_3 = Q(repository__repository_owner__exact=owner)
        query_result = self.filter(condition_1 & condition_2 & condition_3)
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


class IssueCommentsCustomManager(models.Manager):
    def _get_date_condition(self, date):
        if date:
            return datetime.datetime.strptime(date, '%Y-%m-%d').date()
        return None

    def filter_conditions(self, owner, repository, **kwargs):
        condition_1 = Q(issue__repository__repository_name__exact=repository)
        condition_2 = Q(issue__repository__repository_owner__exact=owner)
        query_mapper = dict(
            creation_date=Q(
                issue__creation_date__exact=self._get_date_condition(
                    date=kwargs.get("creation_date")
                )
            ),
            status=Q(issue__status__iexact=kwargs.get("status")),
            number=Q(issue__number__exact=kwargs.get("number")),
            title=Q(issue__title__icontains=kwargs.get("title")),
            description=Q(issue__description__icontains=kwargs.get("description")),
            comment=Q(comment__icontains=kwargs.get("comment")),
        )

        final_query = condition_1 & condition_2
        for field, value_to_search in kwargs.items():
            if value_to_search:
                final_query &= query_mapper.get(field)
        query_result = self.filter(final_query)
        return query_result


class IssueComments(models.Model):
    issue = models.ForeignKey(IssueMetadata, on_delete=models.CASCADE)
    comment = models.TextField(null=True, default=None)
    comment_number = models.CharField(max_length=30, null=False, default='')
    objects = IssueCommentsCustomManager()
