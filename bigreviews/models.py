from django.db import models
from common.models import CommonModel


class Bigreview(CommonModel):
    author = models.ForeignKey(  # 대댓글 작성자
        "users.User",
        on_delete=models.CASCADE,
        related_name="bigreviews_written",  # 작성자 입장에서 해당 작성자가 작성한 대댓글들을 가져올 때 사용할 이름
    )
    parent_review = models.ForeignKey(  # 대댓글이 달린 원본 댓글
        "reviews.Review",
        on_delete=models.CASCADE,
        related_name="bigreviews",  # 원본 댓글의 입장에서 해당 원본 댓글에 달린 대댓글들을 가져올 때 사용할 이름
    )
    content = models.CharField(max_length=140)

    def __str__(self):
        return self.content
