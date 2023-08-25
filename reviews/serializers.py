from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Review
from users.serializers import SemiUserSerializer


class ReviewSerializer(ModelSerializer):
    writer_profile_img = serializers.URLField(
        source="review_author.profileImg", read_only=True
    )
    review_writer = SemiUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


class ReviewAtSerializer(ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")  # 년-월-일 시:분 형식으로 변환
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    writer_profile_img = serializers.URLField(
        source="review_author.profileImg", read_only=True
    )

    class Meta:
        model = Review
        fields = "__all__"
