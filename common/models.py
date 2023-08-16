from django.db import models


class CommonModel(models.Model):

    """Common Model"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_block = models.BooleanField(default=False)

    class Meta:
        abstract = True
