import uuid

from django.db import models

from apps.celebrity.enums import KeywordsEnum, StatusEnum


class Actor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    imdb_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    birthday = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(null=False, blank=False)
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
        db_table = "actor"
        verbose_name = "Actor"
        verbose_name_plural = "Actors"
        ordering = ["-created", "-updated"]
        indexes = [
            models.Index(fields=["name"], name="A_name_idx"),
            models.Index(fields=["status"], name="A_status_idx"),
            models.Index(fields=["created"], name="A_created_idx"),
        ]


class ActorImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    keyword = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=KeywordsEnum.choices,
    )
    url = models.URLField(blank=False, null=False)
    path = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=50,
        default=StatusEnum.READY,
        choices=StatusEnum.choices,
    )
    is_valid = models.BooleanField(blank=True, null=True)
    attempt = models.IntegerField(default=0, null=False, blank=False)
    created = models.DateTimeField(
        null=False, blank=False, auto_now_add=True, editable=False
    )
    updated = models.DateTimeField(null=True, blank=True, auto_now=True, editable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__!r})"

    def __str__(self):
        return f"{self.id}"

    class Meta:
        db_table = "actor_image"
        verbose_name = "Actor image"
        verbose_name_plural = "Actors Images"
        ordering = ["-created", "-updated"]
        indexes = [
            models.Index(fields=["keyword"], name="AI_keyword_idx"),
            models.Index(fields=["url"], name="AI_url_idx"),
            models.Index(fields=["created"], name="AI_created_idx"),
        ]


class ElasticSearchActorImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor_image = models.ForeignKey(ActorImage, on_delete=models.CASCADE)
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
        return f"{self.id}"

    class Meta:
        db_table = "elasticsearch_actor_image"
        verbose_name = "Elasticsearch Actor image"
        verbose_name_plural = "Elasticsearch Actors Images"
        ordering = ["-created", "-updated"]
        indexes = [
            models.Index(fields=["status"], name="EAI_status_idx"),
            models.Index(fields=["created"], name="EAI_created_idx"),
            models.Index(fields=["created", "status"], name="EAI_created_status_idx"),
        ]
