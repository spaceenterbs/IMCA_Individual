from django.urls import path
from . import views

urlpatterns = [
    path("", views.Calendarinfo.as_view()),
    path("<int:pk>", views.CalendarDetail.as_view()),
    path("<int:pk>/memo/", views.Memoapi.as_view()),
    path("<int:pk>/memo/<int:memo_pk>", views.MemoDetail.as_view()),
]
