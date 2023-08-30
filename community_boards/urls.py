from django.urls import path
from . import views

# app_name = "community_boards"  # 다른 애플리케이션과의 URL 패턴 충돌을 방지하고 각각의 애플리케이션의 URL 패턴을 정확히 식별하기 위해 사용  # 이렇게 하면 템플릿에서 {% url 'community_boards:board_detail' board.pk %} 이런 식으로 사용 가능
# # "community_boards" 애플리케이션 내에서 정의된 URL 패턴들의 네임스페이스를 "community_boards"로 지정한 것

urlpatterns = [
    # path("", views.Boards.as_view(), name="boards"),
    # path("<int:pk>/", views.BoardDetail.as_view(), name="board_detail"),
    path("category/<str:category>/", views.CategoryBoards.as_view()),
    path("category/<str:category>/get/", views.UnauthenticatedCategoryBoards.as_view()),
    path("category/<str:category>/<int:pk>/like/", views.CategoryBoardLike.as_view()),
    path(
        "category/<str:category>/<int:pk>/like/get/",
        views.UnauthenticatedCategoryBoardLike.as_view(),
    ),
    # path(
    #     "category/<str:category>/page/<int:page>/",
    #     views.CategoryBoards.as_view(),
    #     name="board_category",
    # ),
    # path(
    #     "category/<str:category>/page/<int:page>/",
    #     views.CategoryBoards.as_view(),
    #     name="board_category_with_pagination",
    # ),
    path(
        "category/<str:category>/detail/<int:pk>/", views.CategoryBoardDetail.as_view()
    ),
    path(
        "category/<str:category>/detail/<int:pk>/get/",
        views.UnauthenticatedCategoryBoardDetail.as_view(),
    ),
    path("category/<str:category>/count", views.CategoryBoardsArrange.as_view()),
    # path(
    #     "category_gather/<str:category>/<int:pk>/",
    #     views.CategoryGatherDetail.as_view(),
    #     name="category_gather_detail",
    # ),
]
