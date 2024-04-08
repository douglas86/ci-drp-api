import asyncio
from adrf.views import APIView
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly


# example of async generator and async coroutine
# https://superfastpython.com/asyncio-async-for/


class ProfileList(APIView):
    model = Profile

    async def async_generator(self):
        profiles = self.model.objects.all()
        yield profiles

    async def async_coroutine(self):
        async for profile in self.async_generator():
            return profile

    def get(self, request):
        profiles = asyncio.run(self.async_coroutine())
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class ProfileDetail(APIView):
    model = Profile
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    def get_object(self, pk):
        try:
            profile = self.model.objects.get(pk=pk)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        profile = self.get_object(pk)
        self.check_object_permissions(request, profile)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
