import asyncio
from adrf.views import APIView
from django.http import Http404
from rest_framework import status, generics, filters
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend


# example of async generator and async coroutine
# https://superfastpython.com/asyncio-async-for/

class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        follwers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
    )
    serializer_class = ProfileSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filterset_fields = ['owner__following__followed__profile', 'owner__followed__owner__profile']
    ordering_fields = ['posts_count', 'followers_count', 'following_count', 'owner__following__created_at',
                       'owner__followed__created_at']


# class ProfileList(APIView):
#     model = Profile
#
#     async def async_generator(self):
#         profiles = self.model.objects.all()
#         yield profiles
#
#     async def async_coroutine(self):
#         async for profile in self.async_generator():
#             return profile
#
#     def get(self, request):
#         profiles = asyncio.run(self.async_coroutine())
#         serializer = ProfileSerializer(profiles, many=True, context={'request': request})
#         return Response(serializer.data)


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        follwers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
    )
    serializer_class = ProfileSerializer
