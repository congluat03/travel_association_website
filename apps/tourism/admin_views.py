from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DiaDiemDuLich, DacSan, TourDuLich, ThuocTour
from .serializers import DiaDiemDuLichSerializer, DacSanSerializer, TourDuLichSerializer, ThuocTourSerializer

# DiaDiemDuLich
@api_view(['GET', 'POST'])
def diadiemdulich_list(request):
    if request.method == 'GET':
        data = DiaDiemDuLich.objects.all()
        serializer = DiaDiemDuLichSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DiaDiemDuLichSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def diadiemdulich_detail(request, pk):
    try:
        obj = DiaDiemDuLich.objects.get(pk=pk)
    except DiaDiemDuLich.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DiaDiemDuLichSerializer(obj)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DiaDiemDuLichSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# DacSan
@api_view(['GET', 'POST'])
def dacsan_list(request):
    if request.method == 'GET':
        data = DacSan.objects.all()
        serializer = DacSanSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DacSanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def dacsan_detail(request, pk):
    try:
        obj = DacSan.objects.get(pk=pk)
    except DacSan.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DacSanSerializer(obj)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DacSanSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# TourDuLich
@api_view(['GET', 'POST'])
def tourdulich_list(request):
    if request.method == 'GET':
        data = TourDuLich.objects.all()
        serializer = TourDuLichSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TourDuLichSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def tourdulich_detail(request, pk):
    try:
        obj = TourDuLich.objects.get(pk=pk)
    except TourDuLich.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TourDuLichSerializer(obj)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TourDuLichSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ThuocTour
@api_view(['GET', 'POST'])
def thuoctour_list(request):
    if request.method == 'GET':
        data = ThuocTour.objects.all()
        serializer = ThuocTourSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ThuocTourSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def thuoctour_detail(request, pk):
    try:
        obj = ThuocTour.objects.get(pk=pk)
    except ThuocTour.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ThuocTourSerializer(obj)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ThuocTourSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
