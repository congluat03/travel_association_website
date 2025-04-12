from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import TinTuc, TheTag, TrackingXemTin
from .serializers import TinTucSerializer, TheTagSerializer, TrackingXemTinSerializer


def handle_list_create(request, model, serializer_class):
    if request.method == 'GET':
        queryset = model.objects.all()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def handle_detail(request, pk, model, serializer_class):
    instance = get_object_or_404(model, pk=pk)

    if request.method == 'GET':
        serializer = serializer_class(instance)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = serializer_class(instance, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- TinTuc ---
@api_view(['GET', 'POST'])
def tintuc_list(request):
    return handle_list_create(request, TinTuc, TinTucSerializer)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def tintuc_detail(request, pk):
    return handle_detail(request, pk, TinTuc, TinTucSerializer)


# --- TheTag ---
@api_view(['GET', 'POST'])
def thetag_list(request):
    return handle_list_create(request, TheTag, TheTagSerializer)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def thetag_detail(request, pk):
    return handle_detail(request, pk, TheTag, TheTagSerializer)


# --- TrackingXemTin ---
@api_view(['GET', 'POST'])
def trackingxemtin_list(request):
    return handle_list_create(request, TrackingXemTin, TrackingXemTinSerializer)

@api_view(['GET', 'PUT', 'DELETE'])
def trackingxemtin_detail(request, pk):
    return handle_detail(request, pk, TrackingXemTin, TrackingXemTinSerializer)
