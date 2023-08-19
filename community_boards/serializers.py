from rest_framework import serializers
from .models import Board, CommonModel
from rest_framework.serializers import ModelSerializer
from users.serializers import SemiUserSerializer


class CommonModelSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")  # 년-월-일 시:분 형식으로 변환
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")  # 년-월-일 시:분 형식으로 변환

    class Meta:
        model = CommonModel
        fields = "__all__"


class BoardSerializer(ModelSerializer):
    author = SemiUserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()  # 추가된 필드
    reviews_count = serializers.SerializerMethodField()  # 추가된 필드

    class Meta:
        model = Board
        fields = "__all__"

    def get_likes_count(self, obj):
        return obj.get_likes_count()  # Board 모델의 get_likes_count 함수 호출

    def get_reviews_count(self, obj):
        return obj.get_reviews_count()  # Board 모델의 get_reviews_count 함수 호출


"""
위의 코드에서 'likes_count'와 'reviews_count' 필드는 serializer의 'SerializerMethodField'를 사용하여 추가되었다.
각 필드의 값을 계산하기 위해 'get_likes_count'와 'get_reviews_count' 함수를 호출하고, 이러한 값을 API 응답에서 사용할 수 있게 된다.

# 따라서 이렇게하면 필드에 값을 저장하지 않고도 게시글의 좋아요 수와 리뷰 수를 API 응답에서 뿌려줄 수 있다.
"""
