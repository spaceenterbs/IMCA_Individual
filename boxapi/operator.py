from apscheduler.schedulers.background import BackgroundScheduler
import time
from . import views


def start():
    scheduler = BackgroundScheduler()

    @scheduler.scheduled_job("cron", day_of_week="mon", hour="12", id="delete")
    def auto_del_data():
        views.del_data()

    @scheduler.scheduled_job("cron", day_of_week="mon", hour="12", id="musical")
    def auto_get_musical():
        try:
            views.get_musical()
        except:
            time.sleep(10)
            views.get_musical()

    @scheduler.scheduled_job("cron", day_of_week="mon", hour="12", id="theater")
    def auto_get_theater():
        try:
            views.get_theater()
        except:
            time.sleep(15)
            views.get_theater()

    scheduler.start()


#  @scheduler.scheduled_job(
#         "cron", day_of_week="fri", hour="17", minute="30", id="theater"
#     )
