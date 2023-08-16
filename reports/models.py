from django.db import models


# class BoardReport(models.Model):
#     board = models.ForeignKey(
#         "community_boards.Board", on_delete=models.CASCADE, related_name="boardreports"
#     )
#     author = models.ForeignKey(
#         "users.User", on_delete=models.CASCADE, related_name="boardreports"
#     )
#     report_user = models.CharField(max_length=30)
#     created_dt = models.DateTimeField(auto_now_add=True)
#     reason = models.TextField()


# class ReviewReport(models.Model):
#     review = models.ForeignKey(
#         "reviews.Review", on_delete=models.CASCADE, related_name="reviewreports"
#     )
#     author = models.ForeignKey(
#         "users.User", on_delete=models.CASCADE, related_name="reviewreports"
#     )
#     report_user = models.CharField(max_length=30)
#     created_dt = models.DateTimeField(auto_now_add=True)
#     reason = models.TextField()


# class BigreviewReport(models.Model):
#     big_review = models.ForeignKey(
#         "bigreviews.Bigreview", on_delete=models.CASCADE, related_name="bigreports"
#     )
#     author = models.ForeignKey(
#         "users.User", on_delete=models.CASCADE, related_name="bigreports"
#     )
#     report_user = models.CharField(max_length=30)
#     created_dt = models.DateTimeField(auto_now_add=True)
#     reason = models.TextField()


class Report(models.Model):
    class ReportCategoryChoices(models.TextChoices):
        게시글 = "board", "게시글"
        댓글 = "review", "댓글"
        대댓글 = "big_review", "대댓글"

    category = models.CharField(max_length=11, choices=ReportCategoryChoices.choices)
    author = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reports"
    )
    reason = models.TextField()
    target_user = models.CharField(max_length=30)
    target_title = models.CharField(max_length=15, null=True, blank=True)
    target_content = models.TextField()
    target_pk = models.PositiveIntegerField()
