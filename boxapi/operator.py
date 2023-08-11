from apscheduler.schedulers.background import BackgroundScheduler
from . import views


def start():
    scheduler = BackgroundScheduler()

    @scheduler.scheduled_job("cron", minute="*/5", id="delete")
    def auto_del_data():
        views.del_data()

    @scheduler.scheduled_job("cron", minute="*/5", id="musical")
    def auto_get_musical():
        views.get_musical()

    @scheduler.scheduled_job("cron", minute="*/5", id="theater")
    def auto_get_theater():
        views.get_theater()

    scheduler.start()


#  @scheduler.scheduled_job(
#         "cron", day_of_week="fri", hour="17", minute="30", id="theater"
#     )
