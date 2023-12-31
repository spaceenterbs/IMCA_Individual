from django.contrib import admin
from .models import Calendar


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
