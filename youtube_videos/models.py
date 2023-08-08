from django.db import models
from common.models import CommonModel


class Youtube_Video(CommonModel):
    title = models.CharField(
        max_length=80,
    )
    content = models.TextField()
    video_url = models.URLField()
    thumbnail_url = models.URLField()
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
