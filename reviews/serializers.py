from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Review
from users.serializers import SemiUserSerializer
from django.contrib.auth.models import AnonymousUser


class ReviewSerializer(ModelSerializer):
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M", read_only=True
    )  # 년-월-일 시:분 형식으로 변환
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    review_writer = SemiUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"

    def create(self, validated_data):
        # 'review_writer' 필드를 현재 사용자 인스턴스 또는 None으로 설정합니다.
        request_user = self.context["request"].user

        if isinstance(request_user, AnonymousUser):
            validated_data["review_writer"] = None
        else:
            validated_data["review_writer"] = request_user

        return super().create(validated_data)
