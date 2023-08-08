from django.db import models
from users.models import User


class PrivateCalender(models.Model):
    start_date = models.DateTimeField(null=False, blank=False)
    end_date = models.DateTimeField(null=False, blank=False)
    poster = models.URLField(null=True, blank=True)
    owner = models.OneToOneField("users.User", on_delete=models.CASCADE)
    place = models.CharField(max_length=15)
    state = models.CharField(max_length=7)
    genre = models.CharField(max_length=7)
    name = models.CharField(max_length=20)


class Memo(models.Model):
    calender = models.ForeignKey(
        "calenders.Privatecalender",
        on_delete=models.CASCADE,
        related_name="memos",
    )
    title = models.CharField(max_length=15)
    content = models.TextField()
