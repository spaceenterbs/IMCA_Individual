from django.db import models


class Calendar(models.Model):
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    selected_date = models.DateField(null=True, blank=True)
    poster = models.URLField(null=True, blank=True)
    place = models.CharField(max_length=50)
    name = models.CharField(max_length=60)
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
    content = models.TextField()
