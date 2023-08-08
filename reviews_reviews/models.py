from django.db import models
from common.models import CommonModel


class Review_Review(CommonModel):
    content = models.CharField(max_length=140)
    is_block = models.BooleanField(default=False)

    def __str__(self):
        return self.content
