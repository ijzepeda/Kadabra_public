# Generated by Django 4.2.1 on 2023-05-31 18:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("celebrity", "0002_alter_actorimage_path"),
    ]

    operations = [
        migrations.AddField(
            model_name="actor",
            name="birthday",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="actor",
            name="gender",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="actor",
            name="nationality",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]