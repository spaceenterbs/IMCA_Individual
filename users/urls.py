from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("Register/", views.UserRegister.as_view()),
    path("Login/", views.UserAuth.as_view()),
    path("Refresh/", TokenRefreshView.as_view()),
]
