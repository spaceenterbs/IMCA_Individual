from django.contrib import admin
from .models import Review_Review


@admin.register(Review_Review)
class Review_ReviewAdmin(admin.ModelAdmin):

    """Review_Review Admin Definition"""

    pass
