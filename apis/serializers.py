from rest_framework.serializers import ModelSerializer
from .models import FestivalModel


class ApiSerializer(ModelSerializer):
    class Meta:
        model = FestivalModel
        fields = "__all__"
