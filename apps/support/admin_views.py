from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TaiLieu
from .serializers import TaiLieuSerializer

# ====== HÀM CHỨC NĂNG ======

def get_all_tailieu():
    queryset = TaiLieu.objects.all()
    return TaiLieuSerializer(queryset, many=True)

def create_tailieu(data):
    serializer = TaiLieuSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_tailieu_by_pk(pk):
    try:
        return TaiLieu.objects.get(pk=pk)
    except TaiLieu.DoesNotExist:
        return None

def update_tailieu(instance, data):
    serializer = TaiLieuSerializer(instance, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def delete_tailieu(instance):
    instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# ====== VIEW CHÍNH ======

@api_view(['GET', 'POST'])
def tailieu_list(request):
    if request.method == 'GET':
        serializer = get_all_tailieu()
        return Response(serializer.data)
    elif request.method == 'POST':
        return create_tailieu(request.data)

@api_view(['GET', 'PUT', 'DELETE'])
def tailieu_detail(request, pk):
    tailieu = get_tailieu_by_pk(pk)
    if not tailieu:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaiLieuSerializer(tailieu)
        return Response(serializer.data)
    elif request.method == 'PUT':
        return update_tailieu(tailieu, request.data)
    elif request.method == 'DELETE':
        return delete_tailieu(tailieu)
