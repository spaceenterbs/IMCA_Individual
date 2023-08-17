from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Board


class BoardSerializer(ModelSerializer):
    likes_num = serializers.SerializerMethodField()
    reviews_num = serializers.SerializerMethodField()

    class Meta:
        model = Board
        exclude = (
            "author",
            "likes_num",
            "reviews_num",
            "views",
        )

    def get_likes_num(self, obj):
        return obj.likes_num.count()

    def get_reviews_num(self, obj):
        return obj.reviews_num.count()
