import os
from pathlib import Path
import environ

root = environ.Path(__file__)
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SITE_ROOT = os.path.abspath(os.path.dirname(__name__))
SECRET_KEY = env("SECRET_KEY", default="")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Application definition

INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
    "django_json_widget",
    "image_uploader_widget",
    "tinymce",
    "constance",
    "rangefilter",
    "phonenumber_field",
    "rest_framework_simplejwt",
    "import_export",
    "django_admin_inline_paginator",
    # Apps
    "apps.celebrity.apps.CelebrityConfig",
    "apps.movies.apps.MoviesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ms_data_mining.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ms_data_mining.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": env.db("DATABASE_URL"),
}
DATABASES["default"]["OPTIONS"] = {"options": "-c search_path=ms_data_mining"}
DATABASES["default"]["CONN_MAX_AGE"] = None

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
STATIC_URL = "static/"

# CORS SECTION
CORS_ORIGIN_ALLOW_ALL = env.bool("CORS_ORIGIN_ALLOW_ALL", default=True)
CORS_ORIGIN_WHITELIST = env("CORS_ORIGIN_WHITELIST").split(",")
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

# REDIS SECTION
REDIS_PORT = env("REDIS_PORT")
REDIS_DB = env("REDIS_DB")
REDIS_DB_RES = env("REDIS_DB_RES")
REDIS_HOST = env("REDIS_HOST")
BROKER_URL = env("CELERY_BROKER_URL")
BROKER_POOL_LIMIT = 3
BROKER_CONNECTION_TIMEOUT = 10

# CELERY SECTION
CELERY_RESULT_BACKEND = "django-db"
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERYD_PREFETCH_MULTIPLIER = 1

# CONSTANCE SECTION
CONSTANCE_ADDITIONAL_FIELDS = {
    "time_type_enum": [
        "django.forms.fields.ChoiceField",
        {
            "widget": "django.forms.Select",
            "choices": (
                ("days", "Days"),
                ("seconds", "Seconds"),
                ("microseconds", "Microseconds"),
                ("milliseconds", "Milliseconds"),
                ("minutes", "Minutes"),
                ("hours", "Hours"),
                ("weeks", "Weeks"),
            ),
        },
    ],
}

CONSTANCE_CONFIG = {
    "CONFIG_ADMIN_LIMIT": (30, "page limit app Alert", int),
    "CONFIG_ADMIN_LISTING_IMAGE_HEIGHT": (100, "Thumbline height in admin page", int),
    "CONFIG_ACTOR_ATTEMPTS": (3, "Actor max attempts", int),
    "CONFIG_IMAGE_ATTEMPTS": (3, "Image max attempts", int),
    "TASK_TIME_TYPE": ("minutes", "select time type", "time_type_enum"),
    "TASK_TIME_VALUE": (5, "Integer number", int),
}

CONSTANCE_CONFIG_FIELDSETS = {
    "Admin Page - Options": (
        "CONFIG_ADMIN_LIMIT",
        "CONFIG_ADMIN_LISTING_IMAGE_HEIGHT",
    ),
    "Actor - Options": ("CONFIG_ACTOR_ATTEMPTS",),
    "Image - Options": ("CONFIG_IMAGE_ATTEMPTS",),
    "Request Task Cache - Options": (
        "TASK_TIME_TYPE",
        "TASK_TIME_VALUE",
    ),
}

IMDBID_APIKEY = env("IMDBID_APIKEY", default="")

ELASTICSEARCH_HOST = env("ELASTICSEARCH_HOST", default="")
ELASTICSEARCH_USER = env("ELASTICSEARCH_USER", default="")
ELASTICSEARCH_PWD = env("ELASTICSEARCH_PWD", default="")
ELASTICSEARCH_VERIFY_CERTS = env.bool("ELASTICSEARCH_VERIFY_CERTS", default=False)
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240
