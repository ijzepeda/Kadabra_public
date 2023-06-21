import uuid

from django.db import models

from apps.celebrity.enums import StatusEnum
from apps.celebrity.models import Actor


class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    imdb_id = models.CharField(null=True, blank=True, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    year = models.TextField(null=True, blank=True)
    rating = models.TextField(null=True, blank=True)
    certificate = models.TextField(null=True, blank=True)
    duration = models.TextField(null=True, blank=True)
    genre = models.TextField(null=True, blank=True)
    votes = models.TextField(null=True, blank=True)
    gross_income = models.TextField(null=True, blank=True)
    director_id = models.TextField(null=True, blank=True)
    director_name = models.TextField(null=True, blank=True)
    starts_id = models.TextField(null=True, blank=True)
    starts_name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    payload = models.JSONField(null=True, blank=True, default=dict)
    status = models.CharField(
        max_length=50,
        default=StatusEnum.READY,
        choices=StatusEnum.choices,
    )
    attempt = models.IntegerField(default=0, null=False, blank=False)
    created = models.DateTimeField(
        null=False, blank=False, auto_now_add=True, editable=False
    )
    updated = models.DateTimeField(null=True, blank=True, auto_now=True, editable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__!r})"

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "movie"
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        ordering = ["-created", "-updated"]
        indexes = [
            models.Index(fields=["name"], name="M_name_idx"),
            models.Index(fields=["imdb_id"], name="M_imdb_id_idx"),
            models.Index(fields=["status"], name="M_status_idx"),
            models.Index(fields=["status", "attempt"], name="M_status_attempt_idx"),
            models.Index(fields=["created"], name="M_created_idx"),
        ]


class MovieActor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie = models.ForeignKey(Movie, on_delete=models.RESTRICT)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    created = models.DateTimeField(
        null=False, blank=False, auto_now_add=True, editable=False
    )
    updated = models.DateTimeField(null=True, blank=True, auto_now=True, editable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__!r})"

    def __str__(self):
        return f"{self.id}"

    class Meta:
        db_table = "movie_actor"
        verbose_name = "Movie Actor"
        verbose_name_plural = "Movies Actors"
        ordering = ["-created", "-updated"]
        indexes = [
            models.Index(fields=["created"], name="MA_created_idx"),
        ]
        unique_together = ["movie", "actor"]
