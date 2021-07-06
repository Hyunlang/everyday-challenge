from rest_framework import serializers
from ..models import Challenge

class SubjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    challengers = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()

    def get_challengers(self, obj):
        challengers = Challenge.objects.filter(subject=obj).count()
        return challengers

    def get_completed(self, obj):
        completed = Challenge.objects.filter(subject=obj, status="complete").count()
        return completed