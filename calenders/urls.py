from django.urls import path
from . import views

urlpatterns = [
    path("", views.Calendarinfo.as_view()),
    path("<int:pk>", views.CalendarDetail.as_view()),
    # path("<int:cal_pk>/memo/", views.Memoapi.as_view()),
]
