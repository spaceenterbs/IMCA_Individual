from django.urls import path
from . import views

urlpatterns = [
    # path(
    #     "",
    #     views.Bigreviews.as_view(),
    #     name="bigreviews",
    # ),
    path(
        "category/<str:category>/",
        views.CategoryBigreviewList.as_view(),
        name="category-bigreview-list",
    ),
]
