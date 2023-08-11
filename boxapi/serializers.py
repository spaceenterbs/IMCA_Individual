from rest_framework import serializers
from .models import BoxMusical, BoxTheater


class MusicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxMusical
        fields = "__all__"


class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxTheater
        fields = "__all__"
