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
    def get(self, request):
        all_bigreviews = Bigreview.objects.all()
        serializer = BigreviewSerializer(
            all_bigreviews,
            many=True,
        )
        return Response(serializer.data)

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
    def get_object(self, pk):
        try:
            return Bigreview.objects.get(pk=pk)
        except Bigreview.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        except Exception as e:
            raise e

    def get(self, request, pk):
        review = self.get_object(pk)
        serializer = BigreviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, pk):
        bigreview = self.get_object(pk)
        serializer = BigreviewSerializer(bigreview, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        bigreview = self.get_object(pk)
        bigreview.delete()
        return Response(status=HTTP_204_NO_CONTENT)
