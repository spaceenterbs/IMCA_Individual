from django.urls import path
from . import views

urlpatterns = [
    path("", views.SaveReport.as_view()),
    path("view/", views.ReportView.as_view()),
    path("<int:pk>/", views.DetailViewReport.as_view()),
]
