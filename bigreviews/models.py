from django.db import models
from common.models import CommonModel


class Bigreview(CommonModel):
    author = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="rreviews"
    )
    parent_review = models.ForeignKey(
        "reviews.Review", on_delete=models.CASCADE, related_name="rreviews"
    )
    content = models.CharField(max_length=140)
    is_block = models.BooleanField(default=False)

    def __str__(self):
        return self.content
