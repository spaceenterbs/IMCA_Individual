from django.urls import path
from . import views

app_name = "community_boards"

urlpatterns = [
    path("", views.Boards.as_view(), name="boards"),
    path("<int:pk>/", views.BoardDetail.as_view(), name="board_detail"),
    path("<int:board_id>/like/", views.BoardLike.as_view(), name="board_like"),
    path(
        "category/<str:category>/",
        views.CategoryBoards.as_view(),
        name="board_category",
    ),
    path(
        "category/<str:category>/count",
        views.CategoryBoardsArrange.as_view(),
        name="category_boards_sort",
    ),
]
