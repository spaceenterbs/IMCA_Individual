from django.apps import AppConfig
from django.conf import settings


class ApisConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apis"


class ApiSchedulerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apischeduler"

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from . import runscheduler

            runscheduler.start()
