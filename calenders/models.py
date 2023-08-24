from django.db import models


class Calendar(models.Model):
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    poster = models.URLField(null=True, blank=True)
    place = models.CharField(max_length=15)
    runtime = models.TimeField(null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="calendars"
    )

    class Meta:
        verbose_name_plural = "calendars"


class Memo(models.Model):
    calendar = models.ForeignKey(
        "calenders.Calendar",
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
