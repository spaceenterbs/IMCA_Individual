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
            "reason",
            "target_pk",
        )


class DetailReportSerializer(serializers.ModelSerializer):
    target_user = UserSerializer(read_only=True)

    class Meta:
        model = Report
        fields = "__all__"
