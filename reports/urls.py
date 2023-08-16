from django.urls import path
from . import views

urlpatterns = [
    path("", views.SaveReport.as_view()),
    path("<int:pk>", views.ViewReport.as_view()),
]
