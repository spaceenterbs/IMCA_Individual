from rest_framework import serializers
from .models import Calendar, Memo


class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = "__all__"


class SemiInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = (
            "start_date",
            "end_date",
            "name",
        )


class DetailInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        exclude = ("id", "owner")
