import asyncio
from adrf.views import APIView, AsyncRequest
from adrf.viewsets import ViewSet
from django.http import Http404
from rest_framework import status, generics, filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend


# example of async generator and async coroutine
# https://superfastpython.com/asyncio-async-for/

# GitHub page for the example of using adrf views
# https://github.com/em1208/adrf

class ProfileList(ViewSet):
    """
    Uses async/await to list all profiles.
    """

    model = Profile
    serializer_class = ProfileSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filterset_fields = ['owner__following__followed__profile', 'owner__followed__owner__profile']
    ordering_fields = ['posts_count', 'followers_count', 'following_count', 'owner__following__created_at',
                       'owner__followed__created_at']
    message = 'This is the async list method of the view set.'

    async def async_generator(self):
        """
        Async generator method.
        Used to fetch all profiles from database.
        :return:
        """
        profiles = self.model.objects.annotate(
            posts_count=Count('owner__post', distinct=True),
            follwers_count=Count('owner__followed', distinct=True),
            following_count=Count('owner__following', distinct=True),
        )
        yield profiles

    async def async_coroutine(self):
        """
        Async coroutine method.
        Used to iterate around profiles from async_generator method
        :return: profiles from async_generator
        """

        async for profile in self.async_generator():
            return profile

    async def list(self):
        """
        Async list method.
        Used to send message to api.
        :return:
        """
        return Response(
            {"message": self.message}, status=status.HTTP_200_OK
        )

    def retrieve(self, request):
        """
        Async retrieve method.
        Used to send data once api endpoint is called.
        :param request:
        :return:
        """

        # runs async coroutine and returns profiles from that method
        profiles = asyncio.run(self.async_coroutine())
        # sterilizes profiles into json data from api
        serializer = ProfileSerializer(profiles, many=True, context={'request': request})

        return Response(serializer.data)


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
