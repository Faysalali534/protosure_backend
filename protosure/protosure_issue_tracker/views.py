from protosure_issue_tracker.models import IssueMetadata
from protosure_issue_tracker.serializers import IssueMetadataSerializer
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
