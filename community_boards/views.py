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
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse


class CustomPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 100


class Boards(APIView):
    pagination_class = CustomPagination

    @extend_schema(
        tags=["게시판 게시글 API"],
        summary="게시글 리스트를 가져옴",
        description="게시판의 모든 게시글을 가져온다.",
        responses={200: BoardSerializer(many=True)},
    )
    def get(self, request):
        boards = Board.objects.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(boards, request)

        serializer = BoardSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
        # page = self.pagination_class.paginate_queryset(
        #     boards, request, view=self
        # )  # request와 view 인스턴스 전달

        # if page is not None:
        #     serializer = BoardSerializer(page, many=True)
        #     return self.pagination_class.get_paginated_response(serializer.data)

        # serializer = BoardSerializer(boards, many=True)
        # res = serializer.data

        # current_url = request.build_absolute_uri()

        # next_page = page.number + 1 if page.has_next() else None
        # prev_page = page.number - 1 if page.has_previous() else None
        # next_url = None
        # prev_url = None
        # if next_page:
        #     next_url = f"{current_url}?page={next_page}"
        # if prev_page:
        #     prev_url = f"{current_url}?page={prev_page}"

        # data = {
        #     "count": boards.count(),
        #     "next": next_url,
        #     "previous": prev_url,
        #     "results": res,
        # }
        # return Response(data)

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

    def get_object(self, pk):
        try:
            return Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        except Exception as e:
            raise e

    # def patch(self, request, pk):
    #     board = self.get_object(pk)
    #     serializer = BoardSerializer(board, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class BoardLike(APIView):
    @extend_schema(
        tags=["게시글 좋아요 API"],
        summary="게시글 좋아요",
        description="게시글에 좋아요를 누른다.",
        responses={200: BoardSerializer()},
    )
    def post(self, request, board_id):
        # 게시글 객체를 가져옴
        board = get_object_or_404(Board, id=board_id)
        # 현재 요청을 보낸 사용자
        user = request.user

        # 사용자가 이미 좋아요를 눌렀다면 좋아요를 취소하고,
        # 그렇지 않으면 좋아요를 추가
        if user in board.likes_num.all():
            board.likes_num.remove(user)
        else:
            board.likes_num.add(user)

        # 페이지 이동 없이 현재 페이지에서 좋아요 토글 후 응답을 반환
        return Response({"likes_num": board.likes_num.count()})

        # # 다음에 이동할 URL을 설정
        # url_next = request.GET.get("next") or reverse(
        #     "community_boards:board_detail", args=[board_id]
        # )
        # # 해당 URL로 리다이렉트
        # return redirect(url_next)

        """
        클라이언트가 게시글에 좋아요를 누를 때, 해당 게시글의 좋아요 상태를 토글하고, 사용자를 원래 페이지로 리다이렉트하는 기능을 구현한 것
        """
