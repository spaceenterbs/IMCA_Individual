from django.db import models
from common.models import CommonModel
from users.models import User
from reviews.models import Review
from bigreviews.models import Bigreview


class Board(CommonModel):
    class CategoryTypeChoices(models.TextChoices):
        자게 = ("free", "자게")
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
    likes_num = models.PositiveIntegerField(default=0)
    # likes_num = models.ManyToManyField(User, related_name="likes_num", default=0)
    # reviews_num = models.ManyToManyField(Review, related_name="reviews_num", blank=True)

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

    def get_likes_num(self):
        """
        Get the number of users who liked this board.
        """
        return self.likes_num.count()

    def get_review_num(self):
        reviews_count = Review.objects.filter(board=self).count()
        bigreviews_count = Bigreview.objects.filter(review__board=self).count()
        return reviews_count + bigreviews_count
