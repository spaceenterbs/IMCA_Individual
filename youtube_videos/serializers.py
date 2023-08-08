from rest_framework.serializers import ModelSerializer
from .models import Youtube_Video


class Youtube_VideoSerializer(ModelSerializer):
    class Meta:
        model = Youtube_Video
        fields = "__all__"
