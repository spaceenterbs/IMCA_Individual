from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import requests, json, xmltodict
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

API_KEY = settings.API_KEY


class GetPublicAPI(APIView):
    """
    공연 목록 불러오기 API
    """

    def get_time(self):
        return timezone.localtime(timezone.now()) - timedelta(weeks=1)

    @extend_schema(
        tags=["공용 캘린더 API"],
        description="공용 캘린더 API",
        parameters=[
            OpenApiParameter(
                name="shcate",
                description="장르 코드",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="prfstate",
                description="공연 상태",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="prfpdfrom",
                description="시작일",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="prfpdto",
                description="종료일",
                required=True,
                type=str,
            ),
        ],
    )
    def get(self, request):
        url = f"http://kopis.or.kr/openApi/restful/pblprfr/?service={API_KEY}"
        shcate = request.GET.get("shcate", None)
        prfstate = request.GET.get("prfstate", None)
        prfpdfrom = request.GET.get("prfpdfrom", None)
        prfpdto = request.GET.get("prfpdto", None)

        params = {
            "cpage": "1",  # 페이지
            "rows": "30",  # 불러올 데이터 갯수
            "shcate": shcate,  # 장르 코드
            "prfstate": prfstate,  # 공연 상태
            "prfpdfrom": prfpdfrom,  # 공연 시작일
            "prfpdto": prfpdto,  # 공연 종료일
            "signgucode": "11",
        }
        response = requests.get(url, params=params)
        xmldata = xmltodict.parse(response.text)
        jsontext = json.dumps(xmldata["dbs"]["db"], ensure_ascii=False)
        return Response(jsontext)


class DetailAPI(APIView):
    @extend_schema(
        tags=["API상세"],
        description="API상세",
        parameters=[
            OpenApiParameter(
                name="mt20id",
                description="공연 코드",
                required=True,
                type=str,
            ),
        ],
    )
    def get(self, request):
        mt20id = request.GET["mt20id"]
        url = (
            f"http://www.kopis.or.kr/openApi/restful/pblprfr/{mt20id}/service={API_KEY}"
        )
        response = requests.get(url)
        return Response(response)
