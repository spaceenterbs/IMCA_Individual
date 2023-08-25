from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Review
from community_boards.models import Board
from bigreviews.models import Bigreview
from bigreviews.serializers import BigreviewSerializer
from bigreviews.views import CategoryBigreviewList
from .serializers import ReviewSerializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from django.shortcuts import get_object_or_404
from django.test import RequestFactory


class CategoryReviewAndBigreviewList(APIView):
    @extend_schema(
        tags=["댓글의 댓글"],
        summary="카테고리별 댓글과 대댓글 목록을 함께 가져옴",
        description="카테고리별 댓글과 대댓글의 목록을 함께 가져온다",
        responses={200: ReviewSerializer(many=True)},
    )
    def get(self, request, category, board_id):  # board_id를 추가로 받습니다.
        # Validate the category input
        if category not in [choice[0] for choice in Board.CategoryType.choices]:
            return Response({"error": "Invalid category"}, status=HTTP_400_BAD_REQUEST)

        # Get the specific board using board_id
        board = get_object_or_404(Board, id=board_id)

        # Get reviews and their bigreviews for the specified board
        reviews = Review.objects.filter(review_board=board)
        review_id = reviews.values_list("id", flat=True)
        bigreviews = Bigreview.objects.filter(bigreview_review__in=review_id)

        # Create a dictionary to store combined data
        combined_data = []

        # Loop through each review
        for review in reviews:
            review_data = ReviewSerializer(review).data

            # Get bigreviews for this review
            review_bigreviews = bigreviews.filter(bigreview_review=review.id)
            bigreview_data = BigreviewSerializer(review_bigreviews, many=True).data

            review_data["bigreviews"] = bigreview_data
            combined_data.append(review_data)

        return Response(combined_data, status=HTTP_200_OK)

    # def post(self, request, category, board_id):
    #     response = CategoryReviewList.as_view()(request, category)
    #     return response

    def post_review(self, request, category, board_id):
        # Validate the category input
        if category not in [choice[0] for choice in Board.CategoryType.choices]:
            return Response({"error": "Invalid category"}, status=HTTP_400_BAD_REQUEST)

        # Get the specific board using board_id
        board = get_object_or_404(Board, id=board_id)

        data = request.data
        data["review_board"] = board.id  # Adjust this based on your logic

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=["댓글"],
        summary="댓글 수정",
        description="댓글을 수정한다.",
        request=ReviewSerializer,
        responses={204: "No Content", 400: "Bad Request"},
    )
    def put_review(self, request, category, board_id, review_id):
        # Validate the category input
        if category not in [choice[0] for choice in Board.CategoryType.choices]:
            return Response({"error": "Invalid category"}, status=HTTP_400_BAD_REQUEST)

        # Get the specific review using review_id
        review = get_object_or_404(Review, id=review_id)

        data = request.data
        serializer = ReviewSerializer(instance=review, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=["댓글"],
        summary="댓글 삭제",
        description="댓글을 삭제한다.",
        responses={204: "No Content"},
    )
    def delete_review(self, request, category, board_id, review_id):
        # Validate the category input
        if category not in [choice[0] for choice in Board.CategoryType.choices]:
            return Response({"error": "Invalid category"}, status=HTTP_400_BAD_REQUEST)

        # Get the specific review using review_id
        review = get_object_or_404(Review, id=review_id)

        review.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class CategoryBoardReviewList(APIView):
    @extend_schema(
        tags=["댓글"],
        summary="카테고리별 모든 댓글 목록을 가져옴",
        description="카테고리별 모든 댓글의 목록을 가져온다",
        responses={200: ReviewSerializer(many=True)},
    )
    def get(self, request, category, board_id):
        # Validate the category input
        if category not in [choice[0] for choice in Board.CategoryType.choices]:
            return Response({"error": "Invalid category"}, status=HTTP_400_BAD_REQUEST)

        # Get reviews for the specified board in the specified category
        reviews = Review.objects.filter(review_board=board_id)

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, HTTP_200_OK)

    @extend_schema(
        tags=["댓글"],
        summary="카테고리별 댓글 작성",
        description="카테고리별 댓글을 작성한다.",
        request=ReviewSerializer,
        responses={201: ReviewSerializer()},
    )
    def post(self, request, category, board_id):
        # Validate the category input
        if category not in [choice[0] for choice in Board.CategoryType.choices]:
            return Response({"error": "Invalid category"}, status=HTTP_400_BAD_REQUEST)

        # Create a new review for the specified board in the specified category
        data = request.data
        data["board"] = board_id

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=["댓글"],
        summary="카테고리별 댓글을 수정",
        description="카테고리별 댓글을 수정한다.",
        request=ReviewSerializer,
        responses={200: ReviewSerializer()},
    )
    def put(self, request, category, board_id):
        # Validate the category input
        if category not in [choice[0] for choice in Board.CategoryType.choices]:
            return Response({"error": "Invalid category"}, status=HTTP_400_BAD_REQUEST)

        # Update reviews for the specified board in the specified category
        reviews = Review.objects.filter(review_board=board_id)

        data = request.data
        for review in reviews:
            if review.id in data:
                review_data = data[review.id]
                serializer = ReviewSerializer(review, data=review_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        return Response({"message": "Reviews updated successfully"}, status=HTTP_200_OK)

    @extend_schema(
        tags=["댓글"],
        summary="카테고리별 댓글 삭제",
        description="카테고리별 댓글을 삭제한다.",
        responses={204: "No Content"},
    )
    def delete(self, request, category, board_id):
        # Validate the category input
        if category not in [choice[0] for choice in Board.CategoryType.choices]:
            return Response({"error": "Invalid category"}, status=HTTP_400_BAD_REQUEST)

        # Delete reviews for the specified board in the specified category
        reviews = Review.objects.filter(review_board=board_id)

        for review in reviews:
            review.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class CategoryReviewList(APIView):
    @extend_schema(
        tags=["댓글"],
        summary="카테고리별 모든 댓글 목록을 가져옴",
        description="카테고리별 모든 댓글의 목록을 가져온다",
        responses={200: ReviewSerializer(many=True)},
    )
    def get(self, request, category):
        # Validate the category input
        if category not in [choice[0] for choice in Board.CategoryType.choices]:
            return Response({"error": "Invalid category"}, status=HTTP_400_BAD_REQUEST)

        # Get reviews for boards in the specified category
        boards = Board.objects.filter(category=category)
        board_id = boards.values_list("id", flat=True)
        reviews = Review.objects.filter(review_board__in=board_id)

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, HTTP_200_OK)

    @extend_schema(
        tags=["댓글"],
        summary="카테고리별 댓글 작성",
        description="카테고리별 댓글을 작성한다.",
        request=ReviewSerializer,
        responses={201: ReviewSerializer()},
    )
    def post(self, request, category):
        # Validate the category input
        if category not in [choice[0] for choice in Board.CategoryType.choices]:
            return Response({"error": "Invalid category"}, status=HTTP_400_BAD_REQUEST)

        # Create a new review for boards in the specified category
        boards = Board.objects.filter(category=category)
        board_id = boards.values_list("id", flat=True)

        data = request.data
        data["board"] = board_id[0]  # You might need to adjust this based on your logic

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=["댓글"],
        summary="카테고리별 댓글을 수정",
        description="카테고리별 댓글을 수정한다.",
        request=ReviewSerializer,
        responses={200: ReviewSerializer()},
    )
    def put(self, request, category):
        # Validate the category input
        if category not in [choice[0] for choice in Board.CategoryType.choices]:
            return Response({"error": "Invalid category"}, status=HTTP_400_BAD_REQUEST)

        # Update reviews for boards in the specified category
        boards = Board.objects.filter(category=category)
        board_id = boards.values_list("id", flat=True)
        reviews = Review.objects.filter(board__in=board_id)

        data = request.data
        for review in reviews:
            if review.id in data:
                review_data = data[review.id]
                serializer = ReviewSerializer(review, data=review_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        return Response({"message": "Reviews updated successfully"}, status=HTTP_200_OK)

    @extend_schema(
        tags=["댓글"],
        summary="카테고리별 댓글 삭제",
        description="카테고리별 댓글을 삭제한다.",
        responses={204: "No Content"},
    )
    def delete(self, request, category):
        # Validate the category input
        if category not in [choice[0] for choice in Board.CategoryType.choices]:
            return Response({"error": "Invalid category"}, status=HTTP_400_BAD_REQUEST)

        # Delete reviews for boards in the specified category
        boards = Board.objects.filter(category=category)
        board_id = boards.values_list("id", flat=True)
        reviews = Review.objects.filter(board__in=board_id)

        for review in reviews:
            review.delete()

        return Response(status=HTTP_204_NO_CONTENT)


# class Reviews(APIView):
#     @extend_schema(
#         tags=["댓글"],
#         summary="모든 댓글의 목록을 가져옴",
#         description="모든 댓글의 목록을 가져온다.",
#         responses={200: ReviewSerializer(many=True)},
#     )
#     def get(self, request):
#         all_reviews = Review.objects.all()
#         serializer = ReviewSerializer(
#             all_reviews,
#             many=True,
#         )
#         return Response(serializer.data)

#     @extend_schema(
#         tags=["댓글"],
#         summary="새 댓글 작성",
#         description="새 댓글을 작성한다.",
#         request=ReviewSerializer,
#         responses={201: ReviewSerializer()},
#     )
#     def post(self, request):
#         try:
#             serializer = ReviewSerializer(data=request.data)
#             if serializer.is_valid():
#                 content = serializer.save()
#                 return Response(ReviewSerializer(content).data, status=HTTP_201_CREATED)
#             else:
#                 return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

#     @extend_schema(
#         tags=["댓글"],
#         summary="댓글을 수정",
#         description="댓글을 수정한다.",
#         request=ReviewSerializer,
#         responses={200: ReviewSerializer()},
#     )
#     def put(self, request, pk):
#         review = self.get_object(pk)
#         serializer = ReviewSerializer(review, data=request.data)
#         if serializer.is_valid():
#             serializer.save(author=request.user)
#             return Response(serializer.data)
#         return Response(serializer.errors)

#     @extend_schema(
#         tags=["댓글"],
#         summary="댓글을 삭제",
#         description="댓글을 삭제한다.",
#         responses={204: "No Content"},
#     )
#     def delete(self, request, pk):
#         review = self.get_object(pk)
#         review.delete()
#         return Response(status=HTTP_204_NO_CONTENT)

#     def get_object(self, pk):
#         try:
#             return Review.objects.get(pk=pk)
#         except Review.DoesNotExist:
#             return Response(status=HTTP_404_NOT_FOUND)
#         except Exception as e:
#             raise e


# from drf_spectacular.utils import extend_schema
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Review
# from .serializers import ReviewSerializer
# from rest_framework.status import (
#     HTTP_201_CREATED,
#     HTTP_204_NO_CONTENT,
#     HTTP_400_BAD_REQUEST,
#     HTTP_404_NOT_FOUND,
#     HTTP_500_INTERNAL_SERVER_ERROR,
# )


# class Reviews(APIView):
#     @extend_schema(
#         tags=["댓글"],
#         summary="모든 댓글 목록을 가져옴",
#         description="모든 댓글의 목록을 가져온다.",
#         responses={200: ReviewSerializer(many=True)},
#     )
#     def get(self, request):
#         all_reviews = Review.objects.all()
#         serializer = ReviewSerializer(
#             all_reviews,
#             many=True,
#         )
#         return Response(serializer.data)

#     @extend_schema(
#         tags=["댓글"],
#         summary="새 댓글 작성",
#         description="새 댓글을 작성한다.",
#         request=ReviewSerializer,
#         responses={201: ReviewSerializer()},
#     )
#     def post(self, request):
#         try:
#             serializer = ReviewSerializer(data=request.data)
#             if serializer.is_valid():
#                 content = serializer.save()
#                 return Response(ReviewSerializer(content).data, status=HTTP_201_CREATED)
#             else:
#                 return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


# class ReviewDetail(APIView):
#     @extend_schema(
#         tags=["댓글"],
#         summary="댓글 내용",
#         description="댓글의 내용을 가져온다.",
#         responses={200: ReviewSerializer()},
#     )
#     def get(self, request, pk):
#         review = self.get_object(pk)
#         serializer = ReviewSerializer(review)
#         return Response(serializer.data)

#     @extend_schema(
#         tags=["댓글"],
#         summary="댓글 수정",
#         description="댓글을 수정한다.",
#         request=ReviewSerializer,
#         responses={200: ReviewSerializer()},
#     )
#     def put(self, request, pk):
#         review = self.get_object(pk)
#         serializer = ReviewSerializer(review, data=request.data)
#         if serializer.is_valid():
#             serializer.save(author=request.user)
#             return Response(serializer.data)
#         return Response(serializer.errors)

#     @extend_schema(
#         tags=["댓글"],
#         summary="댓글 삭제",
#         description="댓글을 삭제한다.",
#         responses={204: "No Content"},
#     )
#     def delete(self, request, pk):
#         review = self.get_object(pk)
#         review.delete()
#         return Response(status=HTTP_204_NO_CONTENT)

#     def get_object(self, pk):
#         try:
#             return Review.objects.get(pk=pk)
#         except Review.DoesNotExist:
#             return Response(status=HTTP_404_NOT_FOUND)
#         except Exception as e:
#             raise e
