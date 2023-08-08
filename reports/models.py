from django.db import models


class Report(models.Model):
    class ContentTypeChoices(models.TextChoices):
        욕설 = "욕설", "욕설"
        도배 = "도배", "도배"
        홍보 = "홍보", "홍보"
        음란성 = "음란성", "음란성"
        기타 = "기타", "기타"
    type = models.CharField(max_length=5, choices=ContentTypeChoices.choices)
    title = models.CharField(max_length=20)
    content = models.TextField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reports")