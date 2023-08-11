from django.urls import path
from . import views

urlpatterns = [
    path("musical", views.MusicalBoxoffice.as_view()),
    path("theater", views.TheaterBoxOffice.as_view()),
]
