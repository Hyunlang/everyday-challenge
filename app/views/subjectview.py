from rest_framework import generics
from rest_framework.views import APIView
from ..models import Subject
from ..response import APIResponse


class SubjectListView(generics.ListAPIView):
    def list(self, request):
        return APIResponse({
            'status': 'ok'
        })


