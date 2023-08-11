from django.urls import path
from . import views

urlpatterns = [
    path("public/", views.GetPublicAPI.as_view()),
    path("detail/", views.DetailAPI.as_view()),
]
