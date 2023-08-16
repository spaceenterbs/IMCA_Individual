from django.db import models
from common.models import CommonModel


class Bigreview(CommonModel):
    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="bigreviews_user",
    )
    parent_review = models.ForeignKey(
        "reviews.Review",
        on_delete=models.CASCADE,
        related_name="bigreviews_review",
    )
    content = models.CharField(max_length=140)

    def __str__(self):
        return self.content
