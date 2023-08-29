from rest_framework import serializers
from .models import Calendar, Memo


class GetMemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        exclude = ("user",)


class MixMemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = ("content",)


class DotInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = (
            "pk",
            "selected_date",
        )


class DetailInfoSerializer(serializers.ModelSerializer):
    memo = GetMemoSerializer(read_only=True, many=True)

    class Meta:
        model = Calendar
        exclude = ("owner",)


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        exclude = ("owner",)
