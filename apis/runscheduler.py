import logging
import requests, json, xmltodict
from . import models
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from django.conf import settings

logger = logging.getLogger(__name__)


def get_time(self):
    return timezone.localtime(timezone.now()) - timedelta(weeks=1)


API_KEY = settings.API_KEY


def get_musical(self, request):
    url = "http://kopis.or.kr/openApi/restful/boxoffice"
    params = {
        "service": API_KEY,
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
    for data in listdata:
        models.BoxMusical.save(
            musical_id=data["mt20id"],
            musical_name=data["prfnm"],
            place=data["prfplcnm"],
            date=data["prfpd"],
            ranking=data["rnum"],
            poster=data["poster"],
        )
    musicalCnt = models.BoxMusical.objects.all().count()
    return Response({"count": musicalCnt})


def get_theater():
    url = "http://kopis.or.kr/openApi/restful/boxoffice"
    params = {
        "service": API_KEY,
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
    for data in listdata:
        models.BoxMusical.save(
            theater_id=data["mt20id"],
            theater_name=data["prfnm"],
            place=data["prfplcnm"],
            date=data["prfpd"],
            ranking=data["rnum"],
            poster=data["poster"],
        )
    theaterCnt = models.BoxTheater.objects.all().count()
    return Response({"count": theaterCnt})


def start():
    def handle(self, *args, **options):
        scheduler = BackgroundScheduler(
            timezone=settings.TIME_ZONE
        )  # BlockingScheduler를 사용할 수도 있습니다.
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            get_musical,
            trigger=CronTrigger(
                day_of_week="wed", hour="12", minute="00"
            ),  # 실행 시간: 매주 수요일 12시
            id="musical",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("금주 뮤지컬 박스오피스")

        scheduler.add_job(
            get_theater,
            trigger=CronTrigger(
                day_of_week="wed", hour="12", minute="00"
            ),  # 실행 시간: 매주 수요일 12시
            id="theater",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("금주 연극 박스오피스")

        try:
            logger.info("스케쥴 시작중..")
            scheduler.start()  # 없으면 동작하지 않습니다.
        except KeyboardInterrupt:
            logger.info("스케쥴 종료중..")
            scheduler.shutdown()
            logger.info("스케쥴이 정상적으로 종료 되었습니다.")
