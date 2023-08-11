from django.db import models


# Create your models here.
class BoxMusical(models.Model):
    musical_id = models.CharField(max_length=20)
    musical_name = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    ranking = models.PositiveIntegerField(null=False, blank=False)
    place = models.CharField(max_length=20)
    poster = models.URLField()


class BoxTheater(models.Model):
    theater_id = models.CharField(max_length=20)
    theater_name = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    ranking = models.PositiveIntegerField(null=False, blank=False)
    place = models.CharField(max_length=20)
    poster = models.URLField()
