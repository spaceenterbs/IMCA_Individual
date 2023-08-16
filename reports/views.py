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
        report = serializers.ReportSerializer(data=request.data)
        report.is_valid(raise_exception=True)
        data = report.save(author=request.user)
        return Response(serializers.ReportSerializer(data).data)


class ViewReport(APIView):
    permission_classes = [IsAdminUser]

    def get_report(self, pk):
        try:
            return Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        report = self.get_report(pk)
        serializer = serializers.DetailReportSerializer(
            report,
            context={"request": request},
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        report = self.get_report(pk)
        report.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)
