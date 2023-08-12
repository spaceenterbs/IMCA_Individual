from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from . import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


class UserRegister(APIView):
    """
    회원가입 API
    """

    @extend_schema(
        tags=["회원가입"],
        description="회원가입",
        responses=serializers.RegisterSerializer,
        examples=[
            OpenApiExample(
                response_only=True,
                summary="회원가입입니다.",
                name="Register",
                value={
                    "login_id": "아이디",
                    "email": "이메일",
                    "password": "패스워드",
                    "nickname": "닉네임",
                    "profileImg": "이미지URL",
                    "gender": "성별",
                    "name": "이름",
                },
            ),
        ],
    )
    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "회원가입에 성공했습니다.",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAuth(APIView):
    """
    로그인 기능
    """

    def post(self, request):
        login_id = request.data.get("login_id")
        password = request.data.get("password")

        try:
            user = User.objects.get(login_id=login_id)
        except User.DoesNotExist:
            raise NotFound

        if not check_password(password, user.password):
            return Response({"message": "비밀번호가 맞지 않습니다."})

        if user:
            serializer = serializers.UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "로그인 성공",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response({"user": user}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        로그아웃
        """
        res = Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)
        res.delete_cookie("access")
        res.delete_cookie("refresh")
        return res
