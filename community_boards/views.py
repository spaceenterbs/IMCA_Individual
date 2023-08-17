from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Board
from .serializers import BoardSerializer
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class Boards(APIView):
    pagination_class = CustomPagination()

    @extend_schema(
        tags=["게시판 게시글 API"],
        summary="게시글 리스트를 가져옴",
        description="게시판의 모든 게시글을 가져온다.",
        responses={200: BoardSerializer(many=True)},
    )
    def get(self, request):
        boards = Board.objects.all()
        page = self.pagination_class.paginate_queryset(boards, request)
        if page is not None:
            serializer = BoardSerializer(page, many=True)
            return self.pagination_class.get_paginated_response(serializer.data)
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=["게시판 게시글 API"],
        summary="게시글을 만든다.",
        description="새로운 게시글을 만든다.",
        request=BoardSerializer,
        responses={201: BoardSerializer()},
    )
    def post(self, request):
        try:
            serializer = BoardSerializer(data=request.data)
            if serializer.is_valid():
                content = serializer.save(author=request.user)
                return Response(BoardSerializer(content).data, status=HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class BoardDetail(APIView):
    def get_object(self, pk):
        try:
            return Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        except Exception as e:
            raise e

    @extend_schema(
        tags=["게시판 게시글 API"],
        summary="상세 게시글을 가져옴.",
        description="게시글의 상세 내용을 가져온다.",
        responses={200: BoardSerializer()},
    )
    def get(self, request, pk):
        board = self.get_object(pk)
        board.views += 1  # 조회수 증가
        board.save()
        serializer = BoardSerializer(board)
        return Response(serializer.data)

    @extend_schema(
        tags=["게시판 게시글 API"],
        summary="게시글을 수정함.",
        description="게시글을 수정한다.",
        request=BoardSerializer,
        responses={200: BoardSerializer()},
    )
    def put(self, request, pk):
        board = self.get_object(pk)
        serializer = BoardSerializer(board, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=["게시판 게시글 API"],
        summary="게시글 삭제",
        description="게시글을 삭제한다.",
        responses={204: "No Content"},
    )
    def delete(self, request, pk):
        board = self.get_object(pk)
        board.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    # def patch(self, request, pk):
    #     board = self.get_object(pk)
    #     serializer = BoardSerializer(board, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
