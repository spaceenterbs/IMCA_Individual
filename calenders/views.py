from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from .models import Calendar
from users.models import User
from .models import Memo
from . import serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


class Calendarinfo(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["마이 캘린더 일정"],
        description="마이 캘린더 일정",
        response=serializers.SemiInfoSerializer,
    )
    def get(self, request):
        calendar = Calendar.objects.filter(owner=request.user)
        serializer = serializers.SemiInfoSerializer(calendar, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=["마이 캘린더 일정 추가"],
        description="마이 캘린더 일정 추가",
        responses=serializers.DetailInfoSerializer,
        examples=[
            OpenApiExample(
                response_only=True,
                summary="마이 캘린더 입니다..",
                name="calendar",
                value={
                    "start_date": "시작일",
                    "end_date": "종료일",
                    "poster": "포스타",
                    "place": "장소",
                    "state": "공연 상태",
                    "genre": "장르",
                    "name": "제목",
                },
            ),
        ],
    )
    def post(self, request):
        serializer = serializers.DetailInfoSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save(owner=request.user)
            serializer = serializers.DetailInfoSerializer(data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class CalendarDetail(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["디테일 일정"],
        description="디테일 일정",
        response=serializers.DetailInfoSerializer,
        parameters=[
            OpenApiParameter(
                name="pk",
                description="일정 값",
                required=True,
                type=str,
            ),
        ],
    )
    def get(self, request, pk):
        calendar = Calendar.objects.get(pk=pk, owner=request.user)
        serializer = serializers.DetailInfoSerializer(calendar)
        return Response(serializer.data)


class Memoapi(APIView):
    permission_classes = [IsAuthenticated]

    def get_cal(self, pk):
        try:
            return Calendar.objects.get(pk=pk)
        except Calendar.DoesNotExist:
            raise NotFound

    @extend_schema(
        tags=["메모 가져오기"],
        description=["pk 값으로 캘린더 가져옵니다"],
        response=serializers.MemoSerializer,
    )
    def get(self, request, pk):
        calendar = self.get_cal(pk)
        print(calendar.memos.all())
        memo = Memo.objects.filter(calendar=calendar)
        serializer = serializers.MemoSerializer(memo)
        return Response(serializer.data)

    @extend_schema(
        tags=["메모 추가"],
        description="메모 추가",
        responses=serializers.MemoSerializer,
        examples=[
            OpenApiExample(
                response_only=True,
                summary="메모 추가 입니다.",
                name="memo",
                value={
                    "title": "제목",
                    "content": "내용",
                    "user": "작성 유저",
                    "calendar": "캘린더",
                },
            ),
        ],
    )
    def post(self, request, pk):
        cal = self.get_cal(pk)
        serializer = serializers.MemoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        datas = serializer.save(calendar=cal, user=request.user)
        serializer = serializers.MemoSerializer(datas)
        return Response(serializer.data)

    @extend_schema(
        tags=["메모 삭제"],
        description=["메모 삭제 기능"],
    )
    def delete(self, request, pk):
        memo = Memo.objects.get(pk=pk)
