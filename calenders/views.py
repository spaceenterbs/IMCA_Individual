from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from . import serializers

class Calenderinfo(APIView):
    permission_classes = [IsAuthenticated]
    pass


# Create your views here.
