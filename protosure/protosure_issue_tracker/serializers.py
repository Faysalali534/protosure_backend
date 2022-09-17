from rest_framework import serializers

from protosure_issue_tracker.models import IssueMetadata


class IssueMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueMetadata
        fields = '__all__'
        depth = 3

    def save(self, repository_info=None):
        if repository_info:
            self.validated_data['repository'] = repository_info
            IssueMetadata.objects.create(**self.validated_data)
