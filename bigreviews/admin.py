from django.contrib import admin
from .models import Bigreview


@admin.register(Bigreview)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
