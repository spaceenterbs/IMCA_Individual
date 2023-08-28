from django.db import models
from common.models import CommonModel

# from users.models import User
# from reviews.models import Review
# from bigreviews.models import Bigreview


class Board(CommonModel):
    class CategoryType(models.TextChoices):
        자게 = ("free", "자게")
        후기 = ("after", "후기")
        양도 = ("trade", "양도")

    writer = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="boards_user",  # 사용자 입장에서 해당 사용자가 작성한 게시글들을 가져올 때 사용할 이름
    )
    Image = models.URLField(blank=True, null=True)  # 이미지
    title = models.CharField(max_length=30, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    category = models.CharField(max_length=12, choices=CategoryType.choices)
    views_count = models.PositiveIntegerField(default=0)
    likes_user = models.ManyToManyField(  # 게시글에 좋아요를 누른 사용자들
        # 이 필드는 ManyToManyField로 선언되었습니다. 이것은 좋아요를 누른 사용자들과 게시글 간의 다대다 관계를 나타냅니다.
        # 위의 코드에서는 blank=True로 설정하여 해당 필드가 비어있을 수 있다는 것을 허용하고, 사용자가 좋아요를 누르지 않은 경우에도 게시글을 생성할 수 있도록 합니다.
        "users.User",
        verbose_name="좋아요 목록",
        blank=True,
        related_name="boards_liked",  # 사용자 입장에서 해당 사용자가 좋아요를 누른 게시글들을 가져올 때 사용할 이름
    )
    is_blocked = models.BooleanField(default=False)

    # reviews_num = models.ForeignKey(  # 게시글에 달린 댓글들
    #     # 이 필드는 ForeignKey로 선언되었습니다. 이것은 각 게시글에 달린 댓글을 나타냅니다.
    #     # Review 모델과 연결되는데, related_name을 사용하여 리뷰 입장에서 해당 게시글을 가져올 때 사용할 이름을 지정합니다. 이 필드도 blank=True, null=True로 설정하여 해당 필드가 비어있을 수 있도록 합니다.
    #     "reviews.Review",
    #     on_delete=models.CASCADE,
    #     verbose_name="댓글 목록",
    #     related_name="boards_reviewed",  # 댓글 입장에서 해당 댓글이 작성된 게시글들을 가져올 때 사용할 이름
    #     blank=True,
    #     null=True,
    # )

    def __str__(self):
        return self.title

    def get_likes_count(self):  # likes_user 필드를 통해 해당 게시글이 받은 좋아요 수를 반환한다.
        # self.likes_user_count()를 호출하여 해당 게시글의 좋아요 수를 계산하고 반환한다.
        likes_count = (
            self.likes_user.count()
        )  # count() 메서드를 사용하여 해당 게시글의 좋아요 수를 계산하고 반환한다.
        return likes_count


'''
    def get_review_num(self):
        reviews_count = Review.objects.filter(board=self).count()
        """
        Review 모델에서 현재 게시글("self")과 연결된 리뷰들을 필터링한다.
        Review 모델의 board 필드가 현재 게시글과 연결되어 있으므로 "board=self" 필터링 조건을 설정한다. 이는 현재 게시글에 연결된 리뷰들을 찾아내기 위함이다.
        .count()는 필터링된 리뷰들의 개수를 반환한다.
        """
        bigreviews_count = Bigreview.objects.filter(review__board=self).count()
        """
        Bigreview 모델에서 현재 게시글("self")과 연결된 리뷰들을 필터링한다.
        Bigreview 모델의 review 필드가 Review 모델과의 관계를 나타내고, Review 모델의 board 필드가 현재 게시글과 연결되어 있다.
        review__board=self라고 필터링 조건을 설정하여, 현재 게시글에 연결된 bigreview들을 찾아낸다.
        .count()는 필터링된 bigreview들의 개수를 반환한다.
        """
        return reviews_count + bigreviews_count
'''

# def get_reviews_count(self):  # 현재 게시글과 연관된 리뷰 및 큰 리뷰의 개수를 계산하고 반환한다.
#     # Review 모델과 Bigreview 모델을 필터링하여 현재 게시글과 연관된 리뷰 및 큰 리뷰의 개수를 계산하고 반환한다.
#     ## 예를 들어 게시글 인스턴스 'my_board'에서 'my_board.get_reviews_count()'를 호출하면, 해당 게시글에 달린 리뷰와 큰 리뷰의 총 개수를 반환한다.
#     reviews_count = Review.objects.filter(board=self).count()
#     bigreviews_count = Bigreview.objects.filter(parent_review__board=self).count()
#     return reviews_count + bigreviews_count
