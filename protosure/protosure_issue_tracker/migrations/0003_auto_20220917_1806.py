# Generated by Django 3.2.15 on 2022-09-17 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('protosure_issue_tracker', '0002_issuemetadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuemetadata',
            name='comment_count',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='IssueComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(default=None, null=True)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='protosure_issue_tracker.repositoryinfo')),
            ],
        ),
    ]
