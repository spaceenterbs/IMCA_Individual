from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Bigreview
from reviews.models import Review
from community_boards.models import Board
from .serializers import BigreviewSerializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


class CategoryBigreviewList(APIView):
    @extend_schema(
        tags=["댓글의 댓글"],
        summary="카테고리별 대댓글 목록을 가져옴",
        description="카테고리별 대댓글의 목록을 가져온다",
        responses={200: BigreviewSerializer(many=True)},
    )
    def get(self, request, category):
        # Validate the category input
        if category not in [choice[0] for choice in Board.CategoryType.choices]:
            return Response({"error": "Invalid category"}, status=HTTP_400_BAD_REQUEST)

        # Get big reviews for parent reviews in the specified category
        parent_reviews = Review.objects.filter(review_board__category=category)
        parent_review_ids = parent_reviews.values_list("id", flat=True)
        bigreviews = Bigreview.objects.filter(bigreview_review__in=parent_review_ids)

        serializer = BigreviewSerializer(bigreviews, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=["댓글의 댓글"],
        summary="카테고리별 대댓글 작성",
        description="카테고리별 새 대댓글을 작성한다.",
        request=BigreviewSerializer,
        responses={201: BigreviewSerializer()},
    )
    def post(self, request, category):
        # Validate the category input
        if category not in [choice[0] for choice in Board.CategoryType.choices]:
            return Response({"error": "Invalid category"}, status=HTTP_400_BAD_REQUEST)

        # Create a new big review for parent reviews in the specified category
        parent_reviews = Review.objects.filter(board__category=category)
        parent_review_ids = parent_reviews.values_list("id", flat=True)

        data = request.data
        data["parent_review"] = parent_review_ids[
            0
        ]  # You might need to adjust this based on your logic

        serializer = BigreviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=["댓글의 댓글"],
        summary="카테고리별 대댓글 수정",
        description="카테고리별 대댓글을 수정한다.",
        request=BigreviewSerializer,
        responses={200: BigreviewSerializer()},
    )
    def put(self, request, category):
        # Validate the category input
        if category not in [choice[0] for choice in Board.CategoryType.choices]:
            return Response({"error": "Invalid category"}, status=HTTP_400_BAD_REQUEST)

        # Update big reviews for parent reviews in the specified category
        parent_reviews = Review.objects.filter(board__category=category)
        parent_review_ids = parent_reviews.values_list("id", flat=True)
        bigreviews = Bigreview.objects.filter(parent_review__in=parent_review_ids)

        data = request.data
        for bigreview in bigreviews:
            if bigreview.id in data:
                bigreview_data = data[bigreview.id]
                serializer = BigreviewSerializer(
                    bigreview, data=bigreview_data, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "Bigreviews updated successfully"},
            HTTP_200_OK,
        )

    @extend_schema(
        tags=["댓글의 댓글"],
        summary="카테고리별 대댓글 삭제",
        description="카테고리별 대댓글을 삭제한다.",
        responses={204: "No Content"},
    )
    def delete(self, request, category):
        # Validate the category input
        if category not in [choice[0] for choice in Board.CategoryType.choices]:
            return Response({"error": "Invalid category"}, status=HTTP_400_BAD_REQUEST)

        # Delete big reviews for parent reviews in the specified category
        parent_reviews = Review.objects.filter(board__category=category)
        parent_review_ids = parent_reviews.values_list("id", flat=True)
        bigreviews = Bigreview.objects.filter(parent_review__in=parent_review_ids)

        for bigreview in bigreviews:
            bigreview.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class Bigreviews(APIView):
    @extend_schema(
        tags=["댓글의 댓글"],
        summary="대댓글 목록을 가져옴",
        description="대댓글의 목록을 가져온다.",
        responses={200: BigreviewSerializer(many=True)},
    )
    def get(self, request):
        all_bigreviews = Bigreview.objects.all()
        serializer = BigreviewSerializer(
            all_bigreviews,
            many=True,
        )
        return Response(serializer.data)

    @extend_schema(
        tags=["댓글의 댓글"],
        summary="대댓글 작성",
        description="새 대댓글을 작성한다.",
        request=BigreviewSerializer,
        responses={201: BigreviewSerializer()},
    )
    def post(self, request):
        try:
            serializer = BigreviewSerializer(data=request.data)
            if serializer.is_valid():
                content = serializer.save(author=request.user)
                return Response(
                    BigreviewSerializer(content).data, status=HTTP_201_CREATED
                )
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        tags=["댓글의 댓글"],
        summary="대댓글 수정",
        description="대댓글을 수정한다.",
        request=BigreviewSerializer,
        responses={200: BigreviewSerializer()},
    )
    def put(self, request, pk):
        bigreview = self.get_object(pk)
        serializer = BigreviewSerializer(bigreview, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @extend_schema(
        tags=["댓글의 댓글"],
        summary="대댓글 삭제",
        description="대댓글을 삭제한다.",
        responses={204: "No Content"},
    )
    def delete(self, request, pk):
        bigreview = self.get_object(pk)
        bigreview.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Bigreview.objects.get(pk=pk)
        except Bigreview.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        except Exception as e:
            raise e


# from drf_spectacular.utils import extend_schema
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Bigreview
# from .serializers import BigreviewSerializer
# from rest_framework.status import (
#     HTTP_201_CREATED,
#     HTTP_204_NO_CONTENT,
#     HTTP_400_BAD_REQUEST,
#     HTTP_404_NOT_FOUND,
#     HTTP_500_INTERNAL_SERVER_ERROR,
# )


# class Bigreviews(APIView):
#     @extend_schema(
#         tags=["댓글의 댓글"],
#         summary="대댓글 목록을 가져오거나 새 대댓글을 작성하거나 수정하거나 삭제한다.",
#         description="대댓글의 목록을 가져오거나 새 대댓글을 작성하거나 수정하거나 삭제한다.",
#         responses={200: BigreviewSerializer(many=True)},
#     )
#     def get(self, request):
#         all_bigreviews = Bigreview.objects.all()
#         serializer = BigreviewSerializer(
#             all_bigreviews,
#             many=True,
#         )
#         return Response(serializer.data)

#     @extend_schema(
#         tags=["댓글의 댓글"],
#         summary="새 대댓글 작성",
#         description="새 대댓글을 작성한다.",
#         request=BigreviewSerializer,
#         responses={201: BigreviewSerializer()},
#     )
#     def post(self, request):
#         try:
#             serializer = BigreviewSerializer(data=request.data)
#             if serializer.is_valid():
#                 content = serializer.save(author=request.user)
#                 return Response(
#                     BigreviewSerializer(content).data, status=HTTP_201_CREATED
#                 )
#             else:
#                 return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


# class BigreviewDetail(APIView):
#     @extend_schema(
#         tags=["댓글의 댓글"],
#         summary="대댓글 내용",
#         description="대댓글의 내용을 가져온다.",
#         responses={200: BigreviewSerializer()},
#     )
#     def get(self, request, pk):
#         review = self.get_object(pk)
#         serializer = BigreviewSerializer(review)
#         return Response(serializer.data)

#     @extend_schema(
#         tags=["댓글의 댓글"],
#         summary="대댓글 수정",
#         description="대댓글을 수정한다.",
#         request=BigreviewSerializer,
#         responses={200: BigreviewSerializer()},
#     )
#     def put(self, request, pk):
#         bigreview = self.get_object(pk)
#         serializer = BigreviewSerializer(bigreview, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)

#     @extend_schema(
#         tags=["댓글의 댓글"],
#         summary="대댓글 삭제",
#         description="대댓글을 삭제한다.",
#         responses={204: "No Content"},
#     )
#     def delete(self, request, pk):
#         bigreview = self.get_object(pk)
#         bigreview.delete()
#         return Response(status=HTTP_204_NO_CONTENT)

#     def get_object(self, pk):
#         try:
#             return Bigreview.objects.get(pk=pk)
#         except Bigreview.DoesNotExist:
#             return Response(status=HTTP_404_NOT_FOUND)
#         except Exception as e:
#             raise e
