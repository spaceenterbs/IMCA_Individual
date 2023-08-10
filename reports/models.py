from django.db import models


class BoardReport(models.Model):
    board = models.ForeignKey(
        "community_boards.Board", on_delete=models.CASCADE, related_name="boardreports"
    )
    author = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="boardreports"
    )
    report_user = models.CharField(max_length=30)
    created_dt = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()


class ReviewReport(models.Model):
    review = models.ForeignKey(
        "reviews.Review", on_delete=models.CASCADE, related_name="reviewreports"
    )
    author = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reviewreports"
    )
    report_user = models.CharField(max_length=30)
    created_dt = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()


class BigreviewReport(models.Model):
    big_review = models.ForeignKey(
        "bigreviews.Bigreview", on_delete=models.CASCADE, related_name="bigreports"
    )
    author = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="bigreports"
    )
    report_user = models.CharField(max_length=30)
    created_dt = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()
