from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from .models import PrivateCalendar
from users.models import User
from .models import Memo
from . import serializers


class Calendarinfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        calendar = PrivateCalendar.objects.filter(owner=request.user)
        serializer = serializers.SemiInfoSerializer(calendar, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.DetailInfoSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save(owner=request.user)
            serializer = serializers.DetailInfoSerializer(data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class CalendarDetail(APIView):
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        user = self.get_user(pk)
        calendar = PrivateCalendar.objects.filter(owner=user)
        serializer = serializers.DetailInfoSerializer(calendar)
        return Response(serializer.data)


# class Memoapi(APIView):
#     def get_cal(self,pk):
#         try:
#             return PrivateCalendar.objects.get(pk = pk)
#         except PrivateCalendar.DoesNotExist:
#             raise NotFound

#     def get(self, request, cal_pk):
#         cal = self.get_cal(cal_pk)
#         memo = Memo.objects.filter()


# Create your views here.
