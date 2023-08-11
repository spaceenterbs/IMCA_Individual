from django.db import models


class PrivateCalendar(models.Model):
    start_date = models.DateTimeField(null=False, blank=False)
    end_date = models.DateTimeField(null=False, blank=False)
    poster = models.URLField(null=True, blank=True)
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="calendars"
    )
    place = models.CharField(max_length=15)
    state = models.CharField(max_length=7)
    genre = models.CharField(max_length=7)
    name = models.CharField(max_length=20)


class Memo(models.Model):
    calendar = models.ForeignKey(
        "calenders.PrivateCalendar",
        on_delete=models.CASCADE,
        related_name="memos",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="memos",
    )
    title = models.CharField(max_length=15)
    content = models.TextField()


class Meta:
    verbose_name_plural = "calendars"
