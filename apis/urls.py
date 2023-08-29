from django.urls import path
from . import views

urlpatterns = [
    path("", views.SavePublicAPI.as_view()),
]
