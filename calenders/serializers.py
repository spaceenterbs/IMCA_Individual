from rest_framework import serializers
from .models import PrivateCalender, Memo

class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = "__all__"

class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateCalender
        fields = ("start_date","end_date","name", "state","genre",)