from django.contrib import admin
from .models import FestivalModel


@admin.register(FestivalModel)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
