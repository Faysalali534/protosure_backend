from rest_framework import serializers

from protosure_issue_tracker.models import IssueMetadata


class IssueMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueMetadata
        fields = '__all__'
        depth = 3