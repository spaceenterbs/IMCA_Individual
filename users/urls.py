from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("Register/", views.UserRegister.as_view()),
    path("Loginout/", views.UserAuth.as_view()),
    path("Refresh/", TokenRefreshView.as_view()),
    path("Verify", TokenVerifyView.as_view()),
    path("info/", views.UserInfo.as_view()),
    path("change/", views.ChangePassword.as_view()),
    # path('google/login', google_login, name='google_login'),
    # path('google/callback/', google_callback, name='google_callback'),
    # path('google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
]
