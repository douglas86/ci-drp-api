import asyncio
from adrf.views import APIView
from django.http import Http404
from rest_framework import status, generics
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly


# example of async generator and async coroutine
# https://superfastpython.com/asyncio-async-for/

class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


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
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
