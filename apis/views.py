from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import requests, json

API_KEY = settings.API_KEY


class GetPublicAPI(APIView):
    """
    공연 목록 불러오기 API
    """

    def get(self, request):
        url = "http://kopis.or.kr/openApi/restful/pblprfr"
        params = {
            "service": API_KEY,
            "cpage": request.GET["cpage"],  # 페이지
            "rows": request.GET["rows"],  # 불러올 데이터 갯수
            "shcate": request.GET["shcate"],  # 장르 코드
            "prfstate": request.GET["prfstate"],  # 공연 상태
            "prfpdfrom": request.GET["prfpdfrom"],  # 공연 시작일
            "prfpdto": request.GET["prfpdto"],  # 공연 종료일
            "signgucode": "11",
        }
        response = requests.get(url, params=params)
        return Response(response.text)


class BoxOfficeAPI(APIView):
    """
    박스 오피스 API
    """

    def get_time(self):
        return timezone.localtime(timezone.now()) - timedelta(weeks=1)

    def get(self, request):
        url = "http://kopis.or.kr/openApi/restful/boxoffice"
        params = {
            "service": API_KEY,
            "area": "11",
            "ststype": "week",
            "catecode": request.GET["catecode"],
            "date": str(self.get_time().date().year)
            + str(self.get_time().date().month).zfill(2)
            + str(self.get_time().date().day),
        }
        print(params)
        response = requests.get(url, params=params)
        return Response(response.text)
