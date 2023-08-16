from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.Reviews.as_view(),
    ),
    path(
        "<int:pk>/",
        views.ReviewDetail.as_view(),
    ),
]
