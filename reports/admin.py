from django.contrib import admin
from .models import Report


# Register your models here.
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
