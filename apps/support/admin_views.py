from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TaiLieu
from .serializers import TaiLieuSerializer

@api_view(['GET', 'POST'])
def tailieu_list(request):
    if request.method == 'GET':
        data = TaiLieu.objects.all()
        serializer = TaiLieuSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TaiLieuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def tailieu_detail(request, pk):
    try:
        tailieu = TaiLieu.objects.get(pk=pk)
    except TaiLieu.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaiLieuSerializer(tailieu)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TaiLieuSerializer(tailieu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        tailieu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
