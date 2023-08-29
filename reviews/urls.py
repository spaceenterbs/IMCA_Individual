from django.urls import path
from . import views
from .views import ReviewCreate, BigreviewCreate

urlpatterns = [
    path(
        "category_gather_review/<str:category>/<int:board_id>/",
        views.CategoryReviewAndBigreviewList.as_view(),
        name="category-gather-review",
    ),
    path(
        "category_gather_review/<str:category>/<int:board_id>/get/",
        views.UnauthenticatedCategoryReviewAndBigreviewList.as_view(),
        name="category-gather-review",
    ),
]
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
# path(
#     "category/<str:category>/<int:board_id>/",
#     views.CategoryBoardReviewList.as_view(),
#     name="category-board-review-list",
# ),
# path(
#     "create/",  # 댓글 생성 API에 접근할 수 있게 된다.
#     ReviewCreate.as_view(),
#     name="create-review",
# ),
# path(
#     "create/",  # 댓글 생성 API에 접근할 수 있게 된다.
#     BigreviewCreate.as_view(),
#     name="create-review",
# ),
# path(
#     "<int:review_board_id>/",
#     views.ReviewList.as_view(),
#     name="review-list",
# ),
