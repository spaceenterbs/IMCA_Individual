from django.db import models


class FestivalModel(models.Model):
    api_id = models.CharField(max_length=50, unique=True)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    poster = models.URLField(null=True, blank=True)
    place = models.CharField(max_length=50)
    name = models.CharField(max_length=60)
