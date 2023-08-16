from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Bigreview
from .serializers import BigreviewSerializer
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


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
        summary="새 대댓글 작성",
        description="새 대댓글을 작성한다.",
        request=BigreviewSerializer,
        responses={201: BigreviewSerializer()},
    )
    def post(self, request):
        try:
            serializer = BigreviewSerializer(data=request.data)
            if serializer.is_valid():
                content = serializer.save()
                return Response(
                    BigreviewSerializer(content).data, status=HTTP_201_CREATED
                )
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class BigreviewDetail(APIView):
    @extend_schema(
        tags=["댓글의 댓글"],
        summary="대댓글 내용",
        description="대댓글의 내용을 가져온다.",
        responses={200: BigreviewSerializer()},
    )
    def get(self, request, pk):
        review = self.get_object(pk)
        serializer = BigreviewSerializer(review)
        return Response(serializer.data)

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
