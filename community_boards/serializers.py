from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Board
from users.serializers import SemiUserSerializer


class BoardSerializer(ModelSerializer):
    author = SemiUserSerializer(read_only=True)
    likes_num = serializers.SerializerMethodField()
    reviews_num = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = "__all__"

    def get_likes_num(self, obj):
        if obj.likes_num is not None:
            return obj.likes_num.all().count()
        return 0  # Default value if likes_num is None

    def get_reviews_num(self, obj):  # 수정: obj 인자 사용
        return obj.get_reviews_count()  # Use the model method to calculate reviews_num
