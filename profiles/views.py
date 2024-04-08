import asyncio
# from rest_framework.views import APIView
from adrf.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer


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
