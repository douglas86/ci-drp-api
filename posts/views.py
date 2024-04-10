from django.db.models import Count
from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions, generics, filters
from .models import Post
from .serializers import PostSerializer
from drf_api.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class PostList(generics.ListCreateAPIView):
    """
    List posts or create a post if logged in
    The perform_create method associates the post with the logged in user.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True),
    ).order_by('-created_at')
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ['owner__followed__owner__profile', 'likes__owner__profile', 'owner__profile']
    search_fields = ['owner__username', 'title']
    ordering_fields = ['comments_count', 'likes_count', 'likes__created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True),
    ).order_by('-created_at')
