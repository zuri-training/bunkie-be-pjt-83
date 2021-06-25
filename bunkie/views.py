from django.shortcuts import render
from .models import Room,Comment
from .serializers import RoomFilter,ProductSerializer,CommentSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes 
from rest_framework.response import Response
from rest_framework import status,generics,permissions
from rest_framework.authentication import BaseAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.utils import translate_validation
from rest_framework.pagination import PageNumberPagination
from .permissions import IsOwnerOrReadOnly

# Create your views here.



############# Room search options ########################

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def room_filter(request):
    paginator = PageNumberPagination()
    paginator.page_size = 5
    
    filterset = RoomFilter(request.GET, queryset=Room.objects.all())
    if not filterset.is_valid():
         raise translate_validation(filterset.errors)

    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = ProductSerializer(queryset, many=True)
    return paginator.get_paginated_response(serializer.data)





############################# Comment section ####################################
class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(name=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]