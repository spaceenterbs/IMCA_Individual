from rest_framework.views import APIView
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.response import Response
from .models import Youtube_Video
from .serializers import Youtube_VideoSerializer
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from django.db.models import F


class Youtube_Videos(APIView):
    def get(self, request):
        youtube_videos = Youtube_Video.objects.all()
        serializer = Youtube_VideoSerializer(youtube_videos, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            serializer = Youtube_VideoSerializer(data=request.data)
            if serializer.is_valid():
                content = serializer.save()
                return Response(
                    Youtube_VideoSerializer(content).data, status=HTTP_201_CREATED
                )
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class Youtube_VideoDetail(APIView):
    def get_object(self, pk):
        try:
            return Youtube_Video.objects.get(pk=pk)
        except Youtube_Video.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        youtube_video = self.get_object(pk)
        # youtube_video.views_count += 1  # Increase the views_count
        # youtube_video.save()  # Save the changes to the database
        Youtube_Video.objects.filter(pk=pk).update(views_count=F("views_count") + 1)
        serializer = Youtube_VideoSerializer(youtube_video)
        return Response(serializer.data)

    def put(self, request, pk):
        youtube_video = self.get_object(pk)
        serializer = Youtube_VideoSerializer(youtube_video, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        youtube_video = self.get_object(pk)
        youtube_video.delete()
        return Response(status=HTTP_404_NOT_FOUND)


# class CountResult(APIView):
#     def get(self, request):
#         results = Youtube_Video.objects.all()
#         count = results.count()
#         return Response(
#             {"count": count},
#         )
