# Generated by Django 4.2.1 on 2023-05-25 17:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("celebrity", "0002_alter_actorimage_path"),
        ("movies", "0007_movie_m_imdb_id_idx_movie_m_status_attempt_idx"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="movieactor",
            unique_together={("movie", "actor")},
        ),
    ]
