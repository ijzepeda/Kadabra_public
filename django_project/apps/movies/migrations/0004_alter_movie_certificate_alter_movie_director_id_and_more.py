# Generated by Django 4.2.1 on 2023-05-25 00:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0003_alter_movie_name_alter_movie_starts_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="certificate",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="director_id",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="director_name",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="duration",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="genre",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="gross_income",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="rating",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="starts_id",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="votes",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="year",
            field=models.TextField(blank=True, null=True),
        ),
    ]
