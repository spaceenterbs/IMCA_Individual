from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import requests, json, xmltodict

API_KEY = settings.API_KEY


class GetPublicAPI(APIView):
    """
    공연 목록 불러오기 API
    """

    def get_time(self):
        return timezone.localtime(timezone.now()) - timedelta(weeks=1)

    # def get(self, request):
    #     url = "http://kopis.or.kr/openApi/restful/pblprfr"
    #     params = {
    #         "service": API_KEY,
    #         "cpage": "1",  # 페이지
    #         "rows": "10",  # 불러올 데이터 갯수
    #         "shcate": "GGGA",  # 장르 코드
    #         "prfstate": "01",  # 공연 상태
    #         "prfpdfrom": "20220101",  # 공연 시작일
    #         "prfpdto": "20220201",  # 공연 종료일
    #         "signgucode": "11",
    #     }
    #     response = requests.get(url, params=params)
    #     xmldata = xmltodict.parse(response.text)
    #     jsontext = json.dumps(xmldata["dbs"]["db"], ensure_ascii=False)
    #     return Response(jsontext)
    def get(self, request):
        url = "http://kopis.or.kr/openApi/restful/boxoffice"
        params = {
            "service": API_KEY,
            "area": "11",
            "ststype": "week",
            "catecode": "AAAA",
            "date": str(self.get_time().date().year)
            + str(self.get_time().date().month).zfill(2)
            + str(self.get_time().date().day),
        }
        response = requests.get(url, params=params)
        xmldata = xmltodict.parse(response.text)
        listdata = list(xmldata["boxofs"]["boxof"])
        print(listdata[0])
        return Response(listdata)


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
        return Response(response)


class DetailAPI(APIView):
    def get(self, request):
        mt20id = request.GET["mt20id"]
        url = f"http://www.kopis.or.kr/openApi/restful/pblprfr/{mt20id}"
        params = {
            "service": API_KEY,
        }
        response = requests.get(url, params=params)
        return Response(response)
