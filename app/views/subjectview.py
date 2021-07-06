from rest_framework import generics
from rest_framework.views import APIView
from ..models import Subject
from ..response import APIResponse
from ..serializers.subject_serializer import SubjectSerializer
from datetime import date


class SubjectListView(generics.ListAPIView):
    def list(self, request):
        subjects = Subject.objects.filter(date=date.today())
        result = []

        for subject in subjects:
            serialized = SubjectSerializer(subject)
            result.append(serialized.data)

        return APIResponse({
            'result': result,
            'status': 'ok'
        })


