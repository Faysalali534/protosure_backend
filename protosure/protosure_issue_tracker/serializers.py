from rest_framework import serializers

from protosure_issue_tracker.models import IssueMetadata


class IssueMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueMetadata
        fields = '__all__'
        depth = 3

    def validate(self, data):
        is_metadata_being_repeated = IssueMetadata.objects.is_metadata_being_repeated(issue_number=data['number'],
                                                                                      repository=self.initial_data[
                                                                                          'repository'])
        if is_metadata_being_repeated:
            raise serializers.ValidationError("The issue is already there with this number")
        return data

    def save(self, repository_info=None):
        if repository_info:
            self.validated_data['repository'] = repository_info
            IssueMetadata.objects.create(**self.validated_data)
