from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from users.serializers import SemiUserSerializer

from .models import Bigreview


class BigreviewSerializer(ModelSerializer):
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M", read_only=True
    )  # 년-월-일 시:분 형식으로 변환
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    bigreview_writer = SemiUserSerializer(read_only=True)

    class Meta:
        model = Bigreview
        fields = "__all__"
