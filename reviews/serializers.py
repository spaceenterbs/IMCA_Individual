from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Review


class ReviewSerializer(ModelSerializer):
    # total_comments = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = "__all__"
