from rest_framework import serializers

from protosure.Signals import insert_comments_to_issue, update_issue
from protosure.custom_exception import concurrencyError
from protosure_issue_tracker.models import IssueMetadata, IssueComments


class IssueMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueMetadata
        fields = '__all__'
        depth = 3

    def update(self, instance, validated_data):
        # This version is used to handle concurrency issue
        initial_version = instance.version
        issue_metadata = IssueMetadata.objects.filter(pk=instance.pk)

        updated = issue_metadata.update(
            title=validated_data.get('title', instance.title),
            status=validated_data.get('status', instance.status),
            description=validated_data.get('description', instance.description),
            version=initial_version + 1

        )
        if not updated:
            raise concurrencyError()
        issue_metadata_instance = IssueMetadata.objects.filter(pk=instance.pk)
        update_issue.send(
            issue_id=self.context["issue_number"],
            sender=self.context["sender"],
            owner=self.context["owner"],
            repo=self.context["repo"],
            data=dict(self.validated_data),
        )

        return issue_metadata_instance[0]

    def validate(self, data):
        if not self.context.get('update_date'):
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
        if self.instance is not None:
            self.instance = self.update(self.instance, self.validated_data)


class IssueCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueComments
        fields = '__all__'
        depth = 4

    def validate(self, data):
        does_issue_number_exist = IssueMetadata.objects.does_issue_number_exist(
            issue_number=self.context["issue_number"],
            owner=self.context["owner"],
            repository=self.context["repo"],
        )

        if not does_issue_number_exist:
            raise serializers.ValidationError("The issue doesnt exist")
        self.context['issue_metadata_instance'] = does_issue_number_exist[0]
        return data

    def create(self, validated_data):
        comment_info = insert_comments_to_issue.send(
            issue_id=self.context["issue_number"],
            sender=self.context["sender"],
            owner=self.context["owner"],
            repo=self.context["repo"],
            data=dict(self.validated_data),
        )
        return IssueComments.objects.create(
            issue=self.context["issue_metadata_instance"],
            comment=self.validated_data["comment"],
            comment_number=comment_info[0][1]["id"],
        )
