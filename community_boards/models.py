from django.db import models
from common.models import CommonModel
from users.models import User
from reviews.models import Review
from bigreviews.models import Bigreview


class Board(CommonModel):
    class CategoryType(models.TextChoices):
        자유 = ("free", "자게")
        후기 = ("after", "후기")
        양도 = ("trade", "양도")

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="boards")
    photo = models.URLField(blank=True, null=True)  # 이미지
    # file = models.FileField(upload_to="file", blank=True)
    title = models.CharField(max_length=30, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    category = models.CharField(max_length=12, choices=CategoryType.choices)
    views = models.PositiveIntegerField(default=0)
    likes_num = models.PositiveIntegerField(default=0)
    reviews_num = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def like(self, user):
        """
        Add an user to the likes_num field.
        """
        if not self.likes_num.filter(pk=user.pk).exists():
            self.likes_num.add(user)
            self.save()

    def unlike(self, user):
        """
        Remove an user from the likes_num field.
        """
        if self.likes_num.filter(pk=user.pk).exists():
            self.likes_num.remove(user)
            self.save()

    # def get_likes_num(self):
    #     """
    #     Get the number of users who liked this board.
    #     """
    #     return self.likes_num.all().count()  # for many to many field
    #     # return self.likes_num  # for PositiveIntegerField

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
