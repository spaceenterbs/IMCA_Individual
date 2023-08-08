from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    유저 회원가입 시리얼라이저
    """

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        login_id = validated_data.get("login_id")
        email = validated_data.get("email")
        password = validated_data.get("password")
        nickname = validated_data.get("nickname")
        profileImg = validated_data.get("profileImg")
        gender = validated_data.get("gender")
        name = validated_data.get("name")

        user = User(
            login_id=login_id,
            email=email,
            nickname=nickname,
            profileImg=profileImg,
            gender=gender,
            name=name,
        )
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    유저의 모든정보를 나타내 주는 시리얼라이저
    """

    class Meta:
        model = User
        fields = "__all__"
