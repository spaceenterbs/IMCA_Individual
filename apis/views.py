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
        print("response test: ", response)
        xmldata = xmltodict.parse(response.text)
        jsontext = json.dumps(xmldata["dbs"]["db"], ensure_ascii=False)
        return Response(jsontext)


class DetailAPI(APIView):
    def get(self, request):
        mt20id = request.GET["mt20id"]
        url = f"http://www.kopis.or.kr/openApi/restful/pblprfr/{mt20id}"
        params = {
            "service": API_KEY,
        }
        response = requests.get(url, params=params)
        return Response(response)
