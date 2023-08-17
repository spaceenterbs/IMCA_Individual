from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


class Reviews(APIView):
    @extend_schema(
        tags=["댓글"],
        summary="모든 댓글 목록을 가져옴",
        description="모든 댓글의 목록을 가져온다.",
        responses={200: ReviewSerializer(many=True)},
    )
    def get(self, request):
        all_reviews = Review.objects.all()
        serializer = ReviewSerializer(
            all_reviews,
            many=True,
        )
        return Response(serializer.data)

    @extend_schema(
        tags=["댓글"],
        summary="새 댓글 작성",
        description="새 댓글을 작성한다.",
        request=ReviewSerializer,
        responses={201: ReviewSerializer()},
    )
    def post(self, request):
        try:
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid():
                content = serializer.save()
                return Response(ReviewSerializer(content).data, status=HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewDetail(APIView):
    @extend_schema(
        tags=["댓글"],
        summary="댓글 내용",
        description="댓글의 내용을 가져온다.",
        responses={200: ReviewSerializer()},
    )
    def get(self, request, pk):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    @extend_schema(
        tags=["댓글"],
        summary="댓글 수정",
        description="댓글을 수정한다.",
        request=ReviewSerializer,
        responses={200: ReviewSerializer()},
    )
    def put(self, request, pk):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)

    @extend_schema(
        tags=["댓글"],
        summary="댓글 삭제",
        description="댓글을 삭제한다.",
        responses={204: "No Content"},
    )
    def delete(self, request, pk):
        review = self.get_object(pk)
        review.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        except Exception as e:
            raise e
