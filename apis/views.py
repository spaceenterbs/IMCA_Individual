from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from .models import FestivalModel
from django.conf import settings
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import timedelta
import requests, json, xmltodict
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

API_KEY = settings.API_KEY


class SavePublicAPI(APIView):
    """
    공연 목록 불러오기 API
    """

    # def get_time(self):
    #     return timezone.localtime(timezone.now()) - timedelta(weeks=1)

    def get(self, request):
        page = request.GET["page"]
        list = FestivalModel.objects.all().order_by("-start_date")
        paginator = Paginator(list, 20)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            page_obj = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            page_obj = paginator.page(page)
        serializer = serializers.ApiSerializer(page_obj, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=["공용 캘린더 API"],
        description="공용 캘린더 API",
        responses=serializers.ApiSerializer,
        examples=[
            OpenApiExample(
                response_only=True,
                summary="API 저장",
                name="API 저장",
                value={
                    "api_id": "API id",
                    "start_date": "시작일",
                    "end_date": "종료일",
                    "poster": "포스터",
                    "place": "장소",
                    "name": "이름",
                },
            ),
        ],
    )
    def post(self, request):
        serializer = serializers.ApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        serializer = serializers.ApiSerializer(data)
        return Response(serializer.data)
