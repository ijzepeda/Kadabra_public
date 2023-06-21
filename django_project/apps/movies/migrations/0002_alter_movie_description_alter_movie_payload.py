# Generated by Django 4.2.1 on 2023-05-25 00:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="payload",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
