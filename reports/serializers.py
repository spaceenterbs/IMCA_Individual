from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Report
from community_boards.models import Board
from reviews.models import Review
from bigreviews.models import Bigreview


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = (
            "category",
            "author",
            "reason",
            "target_user",
            "target_content",
        )


class DetailReportSerializer(serializers.ModelSerializer):
    target_user = UserSerializer(read_only=True)
    target_content = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = "__all__"

    def get_target_content(self, report):
        request = self.context["request"]
        if request.data["category"] == Report.ReportCategoryChoices.게시글:
            content_pk = request.data["target_pk"]
            content = Board.objects.get(pk=content_pk)
            return report.target_content == content.content

        if request.data["category"] == Report.ReportCategoryChoices.댓글:
            content_pk = request.data["target_pk"]
            content = Review.objects.get(pk=content_pk)
            return report.target_content == content.content

        if request.data["category"] == Report.ReportCategoryChoices.대댓글:
            content_pk = request.data["target_pk"]
            content = Bigreview.objects.get(pk=content_pk)
            return report.target_content == content.content
