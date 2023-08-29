from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.views import APIView
from rest_framework.response import Response
from community_boards.models import Board
from .models import Review
from bigreviews.models import Bigreview
from .serializers import ReviewSerializer
from bigreviews.serializers import BigreviewSerializer
from bigreviews.views import CategoryBigreviewList
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
from rest_framework import status
from django.contrib.auth.models import AnonymousUser


class CategoryReviewAndBigreviewList(APIView):
    permission_classes = []  # [IsAuthenticated]

    @extend_schema(
        tags=["댓글과 대댓글"],
        summary="댓글 및 대댓글 작성",
        description="카테고리별 댓글 또는 대댓글을 작성한다.",
        responses={
            201: ReviewSerializer()
        },  # ReviewSerializer 또는 BigreviewSerializer에 맞게 수정
    )
    def post(self, request, category, board_id, review_id=None):
        data = request.data.copy()

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response(
                {"error": "You need to be logged in to post a comment."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Determine the type of comment (Review or Bigreview)
        is_big_review = review_id is not None

        # Choose the appropriate serializer and related models
        if is_big_review:
            serializer = BigreviewSerializer(data=data, context={"request": request})
            related_review_model = Bigreview
            related_writer_field = "bigreview_writer"
            related_review_field = "bigreview_review"
        else:
            serializer = ReviewSerializer(data=data, context={"request": request})
            related_review_model = Review
            related_writer_field = "review_writer"
            related_review_field = "review_board"

        if serializer.is_valid():
            # Convert user id to User instance
            if not isinstance(request.user, AnonymousUser):
                data[related_writer_field] = request.user

            # Validate parent review if it's a big review
            if is_big_review:
                try:
                    related_review = related_review_model.objects.get(pk=review_id)
                    data[related_review_field] = related_review.id
                except related_review_model.DoesNotExist:
                    return Response(
                        {"error": "Parent review does not exist."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            serializer.save(review_board_id=board_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=["댓글과 대댓글"],
        summary="카테고리별 댓글과 대댓글을 수정",
        description="카테고리별 댓글과 대댓글을 수정한다.",
        request=ReviewSerializer,  # 또는 BigreviewSerializer
        responses={200: "수정 성공"},
    )
    def put(self, request, category, board_id):
        review_id = request.data.get("review_id")
        bigreview_id = request.data.get("bigreview_id")
        content = request.data.get("content")

        if not content:
            return Response(
                {"error": "내용을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if review_id:
                review = Review.objects.get(id=review_id, review_board__id=board_id)

                if review.review_writer == request.user or request.user.is_staff:
                    review.review_content = content
                    review.save()
                    return Response(
                        {"message": "댓글이 수정되었습니다."}, status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
                    )
            elif bigreview_id:
                bigreview = Bigreview.objects.get(
                    id=bigreview_id, bigreview_review__review_board__id=board_id
                )

                # 권한 확인 없이 작성자 또는 관리자만 수정 가능
                if bigreview.bigreview_writer == request.user or request.user.is_staff:
                    bigreview.bigreview_content = content
                    bigreview.save()
                    return Response(
                        {"message": "대댓글이 수정되었습니다."}, status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
                    )
            else:
                return Response(
                    {"error": "댓글 또는 대댓글 ID를 입력해주세요."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except (Review.DoesNotExist, Bigreview.DoesNotExist):
            return Response(
                {"error": "해당 댓글 또는 대댓글이 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

    @extend_schema(
        tags=["댓글과 대댓글"],
        summary="카테고리별 댓글과 대댓글 삭제",
        description="카테고리별 댓글과 대댓글을 삭제한다.",
        responses={204: "No Content"},
    )
    def delete(self, request, category, board_id):
        review_id = request.data.get("review_id")
        bigreview_id = request.data.get("bigreview_id")

        if not review_id and not bigreview_id:
            return Response(
                {"error": "댓글 또는 대댓글 ID를 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            if review_id:
                review = Review.objects.get(id=review_id, review_board__id=board_id)

                if review.review_writer == request.user or request.user.is_staff:
                    review.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(
                        {"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
                    )
            elif bigreview_id:
                bigreview = Bigreview.objects.get(
                    id=bigreview_id, bigreview_review__review_board__id=board_id
                )

                # 권한 확인 없이 작성자 또는 관리자만 삭제 가능
                if bigreview.bigreview_writer == request.user or request.user.is_staff:
                    bigreview.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(
                        {"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
                    )
        except (Review.DoesNotExist, Bigreview.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        tags=["댓글과 대댓글"],
        summary="카테고리별 댓글과 대댓글 목록을 함께 가져옴",
        description="카테고리별 댓글과 대댓글의 목록을 함께 가져온다",
        responses={200: ReviewSerializer(many=True)},
        examples=[
            OpenApiExample(
                response_only=True,
                summary="카테고리별 댓글과 대댓글 목록입니다.",
                name="Review&Bigreview",
                value={
                    "id": 1,
                    "writer_profile_img": "null",
                    "created_at": "2023-08-28 14:15",
                    "updated_at": "2023-08-28 14:15",
                    "review_writer": {
                        "nickname": "IMCA",
                        "profileImg": "null",
                        "email": "admin@gmail.com",
                    },
                    "review_content": "11",
                    "is_blocked": "false",
                    "review_board": 1,
                    "bigreviews": [
                        {
                            "id": 1,
                            "created_at": "2023-08-28 14:15",
                            "updated_at": "2023-08-28 14:15",
                            "writer_profile_img": "null",
                            "bigreview_writer": {
                                "nickname": "IMCA",
                                "profileImg": "null",
                                "email": "admin@gmail.com",
                            },
                            "bigreview_content": "1111",
                            "is_blocked": "false",
                            "bigreview_review": 1,
                        }
                    ],
                },
            )
        ],
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
            bigreviews_in_review = bigreviews.filter(bigreview_review=review.id)
            bigreview_data = BigreviewSerializer(bigreviews_in_review, many=True).data

            review_data["bigreviews"] = bigreview_data
            combined_data.append(review_data)

        return Response(combined_data, status=HTTP_200_OK)


# def post(self, request, category, board_id):
#     response = CategoryReviewList.as_view()(request, category)
#     return response

# def post(self, request, category, board_id):
#     # Validate the category input
#     if category not in [choice[0] for choice in Board.CategoryType.choices]:
#         return Response({"error": "Invalid category"}, status=HTTP_400_BAD_REQUEST)

#     # Get the specific board using board_id
#     board = get_object_or_404(Board, id=board_id)

#     data = request.data
#     data["review_board"] = board.id  # Adjust this based on your logic

#     serializer = ReviewSerializer(data=data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=HTTP_201_CREATED)
#     return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# @extend_schema(
#     tags=["댓글"],
#     summary="댓글 수정",
#     description="댓글을 수정한다.",
#     request=ReviewSerializer,
#     responses={204: "No Content", 400: "Bad Request"},
# )
# def put(self, request, category, board_id, review_id):
#     # Validate the category input
#     if category not in [choice[0] for choice in Board.CategoryType.choices]:
#         return Response({"error": "Invalid category"}, status=HTTP_400_BAD_REQUEST)

#     # Get the specific review using review_id
#     review = get_object_or_404(Review, id=review_id)

#     data = request.data
#     serializer = ReviewSerializer(instance=review, data=data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(status=HTTP_204_NO_CONTENT)
#     return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# @extend_schema(
#     tags=["댓글"],
#     summary="댓글 삭제",
#     description="댓글을 삭제한다.",
#     responses={204: "No Content"},
# )
# def delete(self, request, category, board_id, review_id):
#     # Validate the category input
#     if category not in [choice[0] for choice in Board.CategoryType.choices]:
#         return Response({"error": "Invalid category"}, status=HTTP_400_BAD_REQUEST)

#     # Get the specific review using review_id
#     review = get_object_or_404(Review, id=review_id)

#     review.delete()
#     return Response(status=HTTP_204_NO_CONTENT)


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
        # data["review_writer"] = request.user.id
        data["review_board"] = board_id

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer = serializer.save(
                review_writer=request.user
            )  # review_writer=request.user, review_board=board_id
            return Response(ReviewSerializer(serializer).data, status=HTTP_201_CREATED)
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


############################################################################################################


class ReviewCreate(APIView):
    def post(self, request):
        # 클라이언트로부터 받은 데이터로 댓글 생성을 시도한다.
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class BigreviewCreate(APIView):
    def post(self, request):
        # 클라이언트로부터 받은 데이터로 대댓글 생성을 시도합니다.
        serializer = BigreviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # 대댓글을 저장합니다.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewList(APIView):
    def get(self, request, review_board_id):
        # review_board_id를 기반으로 댓글을 조회한다.
        reviews = Review.objects.filter(
            review_board__id=review_board_id
        )  # 특정 게시물의 ID를 가진 댓글을 조회하고자 할 때 사용되는 필터링 조건
        # Review 모델에서 review_board_id 필드가 특정 값과 일치하는 모든 댓글을 조회하고자 한다면 review_board_id=some_board_id ; 특정 게시물의 ID를 넣어주면 된다.

        # 댓글을 직렬화한다.
        review_serializer = ReviewSerializer(reviews, many=True)

        # 대댓글을 직렬화하고 댓글의 하위 항목으로 추가한다.
        for review in reviews:
            bigreviews = Bigreview.objects.filter(bigreview_review=review)
            bigreview_serializer = BigreviewSerializer(bigreviews, many=True)
            review.bigreviews = bigreview_serializer.data  # 여기서 set() 메서드를 사용하여 대댓글을 추가

        return Response(review_serializer.data, status=status.HTTP_200_OK)


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
