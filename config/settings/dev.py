from .base import *

DEBUG = True

WSGI_APPLICATION = "config.wsgi.application"

ALLOWED_HOSTS = ["127.0.0.1", "0.0.0.0"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
