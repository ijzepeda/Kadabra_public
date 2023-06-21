from django.db import models


class KeywordsEnum(models.TextChoices):
    FACE_YOUNG = "face young"
    FACE = " face"
    SIDE_FACE = " side face"
    LOOKING_UP = " looking up"
    LOOKING_DOWN = " looking down"
    WEARING_GLASSES = " wearning glasses"
    HAPPY_FACE = " happy face"
    NOSE = " nose"
    CLOSE_UP = " close up"
    IMDB = "IMDB"


class StatusEnum(models.TextChoices):
    READY = "READY", "Ready"
    RUNNING = "RUNNING", "Running"
    COMPLETED = "COMPLETED", "Completed"
    ERROR = "ERROR", "Error"
    EXPIRED = "EXPIRED", "Expired"
    FORWARDED = "FORWARDED", "Forwarded"
