# Generated by Django 5.0.4 on 2024-06-08 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ats", "0002_job_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="location",
            field=models.TextField(default="Boston"),
            preserve_default=False,
        ),
    ]
