from rest_framework import generics, permissions
from followers.models import Follower
from drf_api.permissions import IsOwnerOrReadOnly
from followers.serializers import FollowerSerializer


class FollowerListAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
