from django.urls import path
from . import views

urlpatterns = [
    # path(
    #     "",
    #     views.Bigreviews.as_view(),
    #     name="bigreviews",
    # ),
    # path(
    #     "category/<str:category>/",
    #     views.CategoryBigreviewList.as_view(),
    #     name="category-bigreview-list",
    # ),
    path(
        "category/<str:category>/<int:review_id>/get/",
        views.UnauthenticatedCategoryReviewBigreviewList.as_view(),
        name="category-bigreview-list",
    ),
    path(
        "category/<str:category>/<int:review_id>/",
        views.CategoryReviewBigreviewList.as_view(),
        name="category-bigreview-list",
    ),
]
