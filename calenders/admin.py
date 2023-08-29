from django.contrib import admin
from .models import Calendar, Memo


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ("__str__",)


@admin.register(Memo)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
