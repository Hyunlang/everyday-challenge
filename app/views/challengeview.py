from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from ..models import *
from ..enums import *
from ..response import APIResponse
import datetime
import json


class ChallengeListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]

    def get_user(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def list(self, request):
        challenges = Challenge.objects.filter(
            user=request.user,
        ).order_by('created')

        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        if year is not None and month is not None:
            challenges = challenges.filter(
                created__year=year,
                created__month=month,
            )

        payload = {
            'challenges': [{
                'subject': {
                    'id': challenge.subject.id,
                    'title': challenge.subject.title
                },
                'status': challenge.status.value
            } for challenge in challenges]
        }

        return APIResponse({
            'status': 'ok',
            'payload': payload
        })


class ChallengeView(APIView):
    def get_user(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def get(self, request):
        mychallenge = Challenge.objects.filter(
            user=self.get_user(request.user.id),
            created__date=datetime.datetime.now().date()
        )

        if mychallenge.exists():
            participant = Challenge.objects.filter(
                subject=mychallenge.subject,
                status=ChallengeStatus.PENDING
            ).count()
            achiever = Challenge.objects.filter(
                subject=mychallenge.subject,
                status=ChallengeStatus.COMPLETE
            ).count()

            return APIResponse({
                'status': 'ok',
                'payload': json.dumps({
                    'challenge': {
                        'subject': {
                            'title': mychallenge[0].subject.title
                        },
                        'status': mychallenge[0].status.value,
                        'participant': participant,
                        'achiever': achiever
                    }
                })
            })

        return APIResponse({
            'status': 'ok',
            'payload': {
                'challenge': None
            }
        })


