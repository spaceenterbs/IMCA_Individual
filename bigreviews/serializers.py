from rest_framework.serializers import ModelSerializer
from .models import Bigreview


class BigreviewSerializer(ModelSerializer):
    class Meta:
        model = Bigreview
        fields = "__all__"
        # fields = (
        #     "id",
        #     "author",
        #     "parent_review",
        #     "content",
        #     "created_at",
        #     "updated_at",
        #     "is_blocked",
        # )


# class BigreviewSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()

#     class Meta:
#         model = Bigreview
#         fields = ["id", "title", "content", "created_at", "user"]

#     def get_user(self, obj):
#         request = self.context.get("request")
#         if request and request.user.is_authenticated:
#             return request.user.username
#         else:
#             return None
