from django.urls import path
from . import views

urlpatterns = [
    # path(
    #     "",
    #     views.Reviews.as_view(),
    #     name="reviews",
    # ),
    # path(
    #     "category/<str:category>/",
    #     views.CategoryReviewList.as_view(),
    #     name="category-review-list",
    # ),
    path(
        "category/<str:category>/<int:board_id>/",
        views.CategoryBoardReviewList.as_view(),
        name="category-board-review-list",
    ),
    # path(
    #     "category_gather_review/<str:category>/<int:board_id>/",
    #     views.CategoryReviewAndBigreviewList.as_view(),
    #     name="category-gather-review",
    # ),
]
