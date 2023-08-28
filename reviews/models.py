from django.db import models
from common.models import CommonModel


class Review(CommonModel):
    review_writer = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="reviews_writer",  # 작성자의 입장에서 해당 작성자가 작성한 리뷰들을 사져올 때 사용할 이름
    )
    review_board = models.ForeignKey(  # board는 게시글 번호
        "community_boards.Board",
        on_delete=models.CASCADE,
        related_name="reviews",  # 게시글의 입장에서 해당 게시글에 달린 리뷰들을 가져올 때 사용할 이름
    )
    review_content = models.CharField(max_length=140)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.review_content

    # def save(self, *args, **kwargs):
    #     # review_writer 필드가 비어 있으면 현재 로그인한 사용자로 설정
    #     if not self.review_writer:
    #         self.review_writer = self.request.user
    #     super().save(*args, **kwargs)
