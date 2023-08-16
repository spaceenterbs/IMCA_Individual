from django.urls import path
from . import views

urlpatterns = [
    path("", views.Boards.as_view(), name="boards"),
    path("<int:pk>/", views.BoardDetail.as_view(), name="board_detail"),
]
