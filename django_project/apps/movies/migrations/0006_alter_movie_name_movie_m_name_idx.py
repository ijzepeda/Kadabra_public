# Generated by Django 4.2.1 on 2023-05-25 01:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0005_remove_movie_m_name_idx_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddIndex(
            model_name="movie",
            index=models.Index(fields=["name"], name="M_name_idx"),
        ),
    ]
