from django.contrib import admin
from .models import Bigreview


@admin.register(Bigreview)
class BigreviewAdmin(admin.ModelAdmin):
    pass
