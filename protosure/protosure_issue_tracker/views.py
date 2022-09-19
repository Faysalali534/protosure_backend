from django.http import Http404

from protosure.custom_exception import ExternalServiceError, concurrencyError
from protosure_issue_tracker.models import IssueMetadata, IssueComments
from protosure_issue_tracker.serializers import IssueMetadataSerializer, IssueCommentsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from protosure.Signals import sync_issues
from rest_framework import status, generics
from rest_framework import exceptions as drf_exceptions
from django.db.utils import IntegrityError as db_constraint


class RepoInfo(APIView):

    def get(self, request, owner, repo, format=None):
        sync_issues.send(sender=request.headers.get('authorization'), owner=owner, repo=repo)
        repo_issues_metadata = IssueMetadata.objects.all()
        serializer = IssueMetadataSerializer(repo_issues_metadata, many=True)
        return Response(serializer.data)


class IssueUpdate(APIView):
    def get_object(self, owner, repo, issue):
        issue_metadata_instance = IssueMetadata.objects.filter(repository__repository_owner__exact=owner,
                                                               repository__repository_name__exact=repo,
                                                               number__exact=issue)
        if issue_metadata_instance:
            return issue_metadata_instance[0]
        raise Http404

    def patch(self, request, owner, repo, issue, format=None):
        try:
            sync_issues.send(sender=request.headers.get('authorization'), owner=owner, repo=repo)
            issue_instance = self.get_object(owner, repo, issue)
            serializer = IssueMetadataSerializer(issue_instance, data=request.data, partial=True,
                                                 context=dict(update_date=True))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except ExternalServiceError as e:
            return Response(dict(error=e.message), status=e.error_code)
        except drf_exceptions.ValidationError as e:
            error_for_field = [e.detail.get(field_data.attname) for field_data in IssueMetadata._meta.fields if
                               e.detail.get(field_data.attname)]

            error_msg = error_for_field[0] if error_for_field else e.detail.get('non_field_errors')

            return Response(dict(error=str(error_msg[0])), status=status.HTTP_400_BAD_REQUEST)
        except db_constraint:
            return Response(dict(error='Status for this issue cannot be closed'), status=status.HTTP_400_BAD_REQUEST)
        except concurrencyError as e:
            return Response(dict(error=e.message), status=e.error_code)


class IssueComment(APIView):

    def post(self, request, owner, repo, issue, format=None):
        sync_issues.send(
            sender=request.headers.get("authorization"), owner=owner, repo=repo
        )
        try:
            serializer = IssueCommentsSerializer(
                data=request.data,
                context=dict(issue_number=issue, owner=owner, sender=request.headers.get('authorization'), repo=repo)
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ExternalServiceError as e:
            return Response(dict(error=e.message), status=e.error_code)
        except drf_exceptions.ValidationError as e:
            # TODO add its test case
            return Response(dict(error=str(e.detail['non_field_errors'][0])), status=status.HTTP_400_BAD_REQUEST)


class IssueDataFilter(generics.ListAPIView):
    serializer_class = IssueCommentsSerializer

    def get_queryset(self):
        owner = self.kwargs.get('owner')
        repo = self.kwargs.get('repo')
        creation_date = self.request.query_params.get('creation_date')
        status = self.request.query_params.get('status')
        number = self.request.query_params.get('number')
        title = self.request.query_params.get('title')
        description = self.request.query_params.get('description')
        comment = self.request.query_params.get('comment')

        return IssueComments.objects.filter_conditions(owner=owner, repository=repo, creation_date=creation_date,
                                                       status=status, number=number, title=title,
                                                       description=description, comment=comment)
