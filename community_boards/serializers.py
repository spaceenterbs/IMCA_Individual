from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Board


class BoardSerializer(ModelSerializer):
    likes_num = serializers.SerializerMethodField()
    reviews_num = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = "__all__"

    def get_like_num(self, obj):
        return obj.likes_num.count()

    def get_review_num(self, obj):
        return obj.reviews_num.count()
