from django.apps import AppConfig


class CelebrityConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.celebrity"

    def ready(self):
        import apps.celebrity.signals  # noqa: F401
