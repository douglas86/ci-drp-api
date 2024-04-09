from rest_framework import generics, permissions
from likes.models import Like
from drf_api.permissions import IsOwnerOrReadOnly
from likes.serializers import LikeSerializer


class LikeList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly, ]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
