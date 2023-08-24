from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .models import Report
from . import serializers
from community_boards.models import Board
from reviews.models import Review
from bigreviews.models import Bigreview


class SaveReport(APIView):
    @extend_schema(tags=["신고하기"], description="신고하기")
    def post(self, request):
        report = serializers.ReportSerializer(
            data=request.data,
        )
        report.is_valid(raise_exception=True)
        print(request.data)
        if request.data["category"] == Report.ReportCategoryChoices.게시글:
            content_pk = request.data["target_pk"]
            content = Board.objects.get(pk=content_pk)
            report.target_user = content.author
            report.target_content = content.content
            report.target_title = content.title
            data = {
                "user": report.target_user,
                "content": report.target_content,
                "title": report.target_title,
            }
            report = report.save(
                author=request.user,
                target_user=data["user"],
                target_content=data["content"],
                target_title=data["title"],
            )

        if request.data["category"] == Report.ReportCategoryChoices.댓글:
            content_pk = request.data["target_pk"]
            content = Review.objects.get(pk=content_pk)
            report.target_user = content.author
            report.target_content = content.content
            report.target_title = None
            data = {
                "user": report.target_user,
                "content": report.target_content,
                "title": report.target_title,
            }
            report = report.save(
                author=request.user,
                target_user=data["user"],
                target_content=data["content"],
                target_title=data["title"],
            )

        if request.data["category"] == Report.ReportCategoryChoices.대댓글:
            content_pk = request.data["target_pk"]
            content = Bigreview.objects.get(pk=content_pk)
            report.target_user = content.author
            report.target_content = content.content
            report.target_title = None
            data = {
                "user": report.target_user,
                "content": report.target_content,
                "title": report.target_title,
            }
            report = report.save(
                author=request.user,
                target_user=data["user"],
                target_content=data["content"],
                target_title=data["title"],
            )

        return Response(serializers.ReportSerializer(report).data)


class ReportView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(tags=["신고하기"], description="신고하기")
    def get(self, request):
        report = Report.obejcts.all()
        serializer = serializers.DetailReportSerializer(report)
        return Response(serializer.data)


class DetailViewReport(APIView):
    permission_classes = [IsAdminUser]

    def get_report(self, pk):
        try:
            return Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            raise NotFound

    @extend_schema(tags=["신고하기"], description="신고하기")
    def get(self, request, pk):
        report = self.get_report(pk)
        serializer = serializers.DetailReportSerializer(report)
        return Response(serializer.data)

    @extend_schema(tags=["신고하기"], description="신고하기")
    def delete(self, request, pk):
        report = self.get_report(pk)
        if report.category == Report.ReportCategoryChoices.게시글:
            board = Board.objects.get(pk=report.target_pk)
            board.delete()
            report.delete()
        if report.category == Report.ReportCategoryChoices.댓글:
            review = Review.objects.get(pk=report.target_pk)
            review.delete()
            report.delete()
        if report.category == Report.ReportCategoryChoices.대댓글:
            big_review = Bigreview.objects.get(pk=report.target_pk)
            big_review.delete()
            report.delete()
        return Response({"ok": status.HTTP_204_NO_CONTENT})
