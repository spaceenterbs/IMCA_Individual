from django.db import models
from common.models import CommonModel
from users.models import User
from reviews.models import Review


class Board(CommonModel):
    class CategoryTypeChoices(models.TextChoices):
        자게 = ("freeboard", "자게")
        후기 = ("after", "후기")
        양도 = ("trade", "양도")

    author = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="boards"
    )
    photo = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to="file", blank=True)
    title = models.CharField(max_length=30, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    category = models.CharField(max_length=12, choices=CategoryTypeChoices.choices)
    views = models.PositiveIntegerField(default=0)
    likes_num = models.ManyToManyField(User, related_name="likes_num")
    reviews_num = models.ManyToManyField(Review, related_name="reviews_num")

    def __str__(self):
        return self.title

    def get_review_num(self):
        reviews_count = self.reviews_num.count()
        bigreviews_count = 0
        for review in self.reviews_num.all():
            bigreviews_count += review.bigreviews_num.count()
        return reviews_count + bigreviews_count
