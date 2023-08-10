from rest_framework import serializers
from .models import PrivateCalendar, Memo


class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = "__all__"


class SemiInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateCalendar
        fields = (
            "start_date",
            "end_date",
            "name",
            "state",
            "genre",
        )


class DetailInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateCalendar
        fields = "__all__"
