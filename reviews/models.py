from django.db import models
from common.models import CommonModel


class Review(CommonModel):
    author = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reviews"
    )
    board = models.ForeignKey(
        "community_boards.Board", on_delete=models.CASCADE, related_name="reviews"
    )
    content = models.CharField(max_length=140)

    def __str__(self):
        return self.content
