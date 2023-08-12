import logging
import requests, json, xmltodict
import datetime
from . import models
from . import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from drf_spectacular.utils import extend_schema

logger = logging.getLogger(__name__)


def get_time():
    return timezone.localtime(timezone.now()) - timedelta(weeks=1)


API_KEY = settings.API_KEY


def del_data():
    mu_data = models.BoxMusical.objects.all()
    thea_data = models.BoxTheater.objects.all()
    if mu_data:
        mu_data.delete()
    if thea_data:
        thea_data.delete()
    if not mu_data and not thea_data:
        print({"data": "데이터가 없습니다."})


def get_musical():
    url = f"http://kopis.or.kr/openApi/restful/boxoffice?service={API_KEY}"
    params = {
        "area": "11",
        "ststype": "week",
        "catecode": "GGGA",
        "date": str(get_time().date().year)
        + str(get_time().date().month).zfill(2)
        + str(get_time().date().day),
    }
    response = requests.get(url, params=params)
    xmldata = xmltodict.parse(response.text)
    listdata = list(xmldata["boxofs"]["boxof"])
    for data in listdata[0:10]:
        date = data["prfpd"].split("~")
        start = date[0].split(".")
        start_date = "-".join(start)
        end = date[1].split(".")
        end_date = "-".join(end)
        models.BoxMusical(
            musical_id=data["mt20id"],
            musical_name=data["prfnm"],
            place=data["prfplcnm"],
            start_date=datetime.datetime.strptime(start_date, "%Y-%m-%d"),
            end_date=datetime.datetime.strptime(end_date, "%Y-%m-%d"),
            ranking=data["rnum"],
            poster=data["poster"],
        ).save()
    musicalCnt = models.BoxMusical.objects.all().count()
    print({"count": musicalCnt})


def get_theater():
    url = f"http://kopis.or.kr/openApi/restful/boxoffice?service={API_KEY}"
    params = {
        "area": "11",
        "ststype": "week",
        "catecode": "AAAA",
        "date": str(get_time().date().year)
        + str(get_time().date().month).zfill(2)
        + str(get_time().date().day),
    }
    response = requests.get(url, params=params)
    xmldata = xmltodict.parse(response.text)
    listdata = list(xmldata["boxofs"]["boxof"])
    for data in listdata[0:10]:
        date = data["prfpd"].split("~")
        start = date[0].split(".")
        start_date = "-".join(start)
        end = date[1].split(".")
        end_date = "-".join(end)
        models.BoxTheater(
            theater_id=data["mt20id"],
            theater_name=data["prfnm"],
            place=data["prfplcnm"],
            start_date=datetime.datetime.strptime(start_date, "%Y-%m-%d"),
            end_date=datetime.datetime.strptime(end_date, "%Y-%m-%d"),
            ranking=data["rnum"],
            poster=data["poster"],
        ).save()
    theaterCnt = models.BoxTheater.objects.all().count()
    print({"count": theaterCnt})


class MusicalBoxoffice(APIView):
    """
    뮤지컬 박스 오피스 가져오기 API
    """

    @extend_schema(
        tags=["뮤지컬 박스 오피스"],
        description="뮤지컬 박스 오피스",
    )
    def get(self, request):
        musical_data = models.BoxMusical.objects.all()
        serializer = serializers.MusicalSerializer(musical_data, many=True)
        return Response(serializer.data)


class TheaterBoxOffice(APIView):
    """
    연극 박스 오피스 가져오기 API
    """

    @extend_schema(
        tags=["연극 박스 오피스"],
        description="연극 박스 오피스",
    )
    def get(self, request):
        theater_data = models.BoxTheater.objects.all()
        serializer = serializers.TheaterSerializer(theater_data, many=True)
        return Response(serializer.data)
