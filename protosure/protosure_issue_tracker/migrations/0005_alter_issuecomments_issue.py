# Generated by Django 3.2.15 on 2022-09-18 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('protosure_issue_tracker', '0004_issuecomments_comment_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuecomments',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='protosure_issue_tracker.issuemetadata'),
        ),
    ]
