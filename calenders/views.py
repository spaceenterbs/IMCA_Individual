from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Calendar
from users.models import User
from .models import Memo
from . import serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


class Calendarinfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["마이 캘린더 일정"],
        description="마이 캘린더 일정",
        responses=serializers.DetailInfoSerializer,
    )
    def get(self, request):
        calendar = Calendar.objects.filter(owner=request.user)
        serializer = serializers.DotInfoSerializer(calendar, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=["마이 캘린더 일정"],
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
                    "runtime": "상영시간",
                    "price": "가격",
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


class CalendarMenu(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date = request.GET["date"]
        cal = Calendar.objects.filter(selected_date=date).filter(owner=request.user)
        serializer = serializers.MenuSerializer(cal, many=True)
        return Response(serializer.data)


class CalendarDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["디테일 일정"],
        description="디테일 일정",
        responses=serializers.DetailInfoSerializer,
        parameters=[
            OpenApiParameter(
                name="pk",
                description="일정 값",
                required=True,
                type=str,
            ),
        ],
    )
    # def get(self, request, pk):
    #     calendar = Calendar.objects.get(pk=pk)
    #     if calendar.owner != request.user:
    #         raise PermissionError
    #     serializer = serializers.DetailInfoSerializer(calendar)
    #     return Response(serializer.data)

    @extend_schema(
        tags=["디테일 일정"],
        description="일정 삭제",
    )
    def delete(self, request, pk):
        calendar = Calendar.objects.get(pk=pk)
        if calendar.owner != request.user:
            raise PermissionError

        calendar.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)


class Memoapi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_cal(self, pk):
        try:
            return Calendar.objects.get(pk=pk)
        except Calendar.DoesNotExist:
            raise NotFound

    @extend_schema(
        tags=["메모 가져오기"],
        description=["pk 값으로 캘린더 가져옵니다"],
        responses=serializers.GetMemoSerializer,
    )
    def get(self, request, pk):
        calendar = self.get_cal(pk)
        memo = calendar.memos.all()
        # memo = Memo.objects.filter(calendar=calendar)
        serializer = serializers.GetMemoSerializer(memo, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=["메모 추가"],
        description="메모 추가",
        responses=serializers.MixMemoSerializer,
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
        serializer = serializers.MixMemoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        datas = serializer.save(calendar=cal, user=request.user)
        serializer = serializers.MixMemoSerializer(datas)
        return Response(serializer.data)


class MemoDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_cal(self, pk):
        try:
            return Calendar.objects.get(pk=pk)
        except Calendar.DoesNotExist:
            raise NotFound

    def get_memo(self, memo_pk, cal):
        try:
            return Memo.objects.get(pk=memo_pk, calendar=cal)
        except:
            raise NotFound

    @extend_schema(
        tags=["메모 수정"],
        description="메모 수정",
        responses=serializers.MixMemoSerializer,
        examples=[
            OpenApiExample(
                response_only=True,
                summary="메모 수정 입니다.",
                name="memo",
                value={
                    "content": "내용",
                },
            ),
        ],
    )
    def put(self, request, pk, memo_pk):
        cal = self.get_cal(pk)
        memo = self.get_memo(memo_pk, cal)
        if cal.owner != request.user:
            raise PermissionError
        serializer = serializers.MixMemoSerializer(
            memo,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        update = serializer.save()
        return Response(serializers.MixMemoSerializer(update).data)

    @extend_schema(
        tags=["메모 삭제"],
        description="메모 삭제",
    )
    def delete(self, request, pk, memo_pk):
        cal = self.get_cal(pk)
        memo = self.get_memo(memo_pk, cal)
        if cal.owner != request.user:
            raise PermissionError
        try:
            memo.delete()
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            raise ParseError("삭제 실패")
