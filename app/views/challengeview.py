from rest_framework import generics
from rest_framework.views import APIView


class ChallengeListView(generics.ListAPIView):
    def list(self, request):
        pass