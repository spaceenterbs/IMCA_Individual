from django.contrib import admin
from .models import Youtube_Video


@admin.register(Youtube_Video)
class Youtube_VideoAdmin(admin.ModelAdmin):
    pass
