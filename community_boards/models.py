from django.db import models
from common.models import CommonModel


class Board(CommonModel):
    class CategoryTypeChoices(models.TextChoices):
        자게 = ("freeboard", "자게")
        후기 = ("after", "후기")
        양도 = ("trade", "양도")

    title = models.CharField(max_length=30, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    is_block = models.BooleanField(default=False)
    photo = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to="file", blank=True)
    author = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="boards"
    )
    category = models.CharField(max_length=12, choices=CategoryTypeChoices.choices)
