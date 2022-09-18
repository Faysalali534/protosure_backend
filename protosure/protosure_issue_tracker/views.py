from protosure_issue_tracker.models import IssueMetadata
from protosure_issue_tracker.serializers import IssueMetadataSerializer, IssueCommentsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from protosure.Signals import sync_issues


# Create your views here.
class RepoInfo(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, owner, repo, format=None):
        sync_issues.send(sender=request.headers.get('authorization'), owner=owner, repo=repo)
        repo_issues_metadata = IssueMetadata.objects.all()
        serializer = IssueMetadataSerializer(repo_issues_metadata, many=True)
        return Response(serializer.data)


# Create your views here.
class IssueComment(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def post(self, request, owner, repo, issue, format=None):
        sync_issues.send(
            sender=request.headers.get("authorization"), owner=owner, repo=repo
        )
        serializer = IssueCommentsSerializer(
            data=request.data, context=dict(issue_number=issue, owner=owner, repo=repo)
        )
        serializer.is_valid(raise_exception=False)
        serializer.save()
        return Response(serializer.data)

