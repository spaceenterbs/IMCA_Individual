from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Board
from users.serializers import SemiUserSerializer


class BoardSerializer(ModelSerializer):
    author = SemiUserSerializer(read_only=True)
    likes_num = serializers.IntegerField()
    reviews_num = serializers.SerializerMethodField()
    # likes_num 필드는 User 모델과의 다대다 관계를 나타내는 필드이며, reviews_num 필드는 Review 모델과의 다대다 관계를 나타내는 필드입니다. 이러한 필드는 직렬화할 때 불필요한 정보를 노출시킬 수 있으므로,
    # SerializerMethodField를 사용하여 필요한 정보만 계산하여 직렬화하도록 설정하는 것이 좋습니다.

    class Meta:
        model = Board
        fields = "__all__"

    def get_likes_num(self, obj):
        return obj.likes_num.count()

    def get_reviews_num(self, obj):
        return obj.reviews_num()  # Use the model method to calculate reviews_num
