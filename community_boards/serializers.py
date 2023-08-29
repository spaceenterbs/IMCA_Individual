from rest_framework import serializers
from .models import Board
from reviews.models import Review
from bigreviews.models import Bigreview
from users.serializers import SemiUserSerializer


class BoardSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M", read_only=True
    )  # 년-월-일 시:분 형식으로 변환
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    likes_count = serializers.SerializerMethodField()  # 추가된 필드
    reviews_count = serializers.SerializerMethodField()
    writer = SemiUserSerializer(
        read_only=True
    )  # serializer에서는 writer를 SemiUserSerializer로 표현

    class Meta:
        model = Board
        fields = "__all__"

    def create(self, validated_data):
        # Retrieve the category from the URL parameters
        category = self.context["request"].parser_context["kwargs"]["category"]

        # Assign the writer and category to the board
        validated_data["writer"] = self.context["request"].user
        validated_data["category"] = category

        # Save the new board instance
        board = Board.objects.create(**validated_data)
        return board

    def get_likes_count(self, obj):
        return obj.get_likes_count()  # Board 모델의 get_likes_count 함수 호출

    def get_reviews_count(self, obj):  # 추가된 필드 앞에 get_를 붙여줘야 한다.
        reviews = obj.reviews.all()
        total_comments_count = sum(
            review.bigreviews.count() + 1 for review in reviews
        )  # 반복문의 review는 임시 변수
        return total_comments_count

        # obj.reviews.all()로 해당 게시글의 모든 리뷰를 가져온 후, 각 리뷰의 bigreviews.count()를 더한 후 1을 더하여 총 댓글 수를 계산

    # def get_reviews_count(self, obj):
    #     # 해당 Board에 연결된 리뷰와 대댓글의 총 개수 계산
    #     reviews_count = obj.reviews.count()  # 리뷰 수 계산
    #     bigreviews_count = obj.bigreviews.count()  # 대댓글 수 계산
    #     total_comments_count = reviews_count + bigreviews_count  # 총 댓글 수 계산
    #     return total_comments_count

    # def get_reviews_count(self, obj):
    #     return obj.get_reviews_count()  # Board 모델의 get_reviews_count 함수 호출


# class PaginationSerializer(serializers.Serializer):
#     count = serializers.IntegerField()
#     next = serializers.CharField(allow_null=True)
#     previous = serializers.CharField(allow_null=True)
#     results = serializers.ListField(child=serializers.DictField())


"""
위의 코드에서 'likes_count'와 'reviews_count' 필드는 serializer의 'SerializerMethodField'를 사용하여 추가되었다.
각 필드의 값을 계산하기 위해 'get_likes_count'와 'get_reviews_count' 함수를 호출하고, 이러한 값을 API 응답에서 사용할 수 있게 된다.

# 따라서 이렇게하면 필드에 값을 저장하지 않고도 게시글의 좋아요 수와 리뷰 수를 API 응답에서 뿌려줄 수 있다.
"""
