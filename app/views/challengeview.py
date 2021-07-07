from rest_framework import generics
from rest_framework.views import APIView
from django.http import HttpResponse
from ..models import *
from ..enums import *
from ..response import APIResponse
import json
import datetime


class ChallengeListView(generics.ListAPIView):
    def list(self, request):
        challenges = Challenge.objects.filter(
            user=request.user,
        ).order_by('created')

        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        if year is not None and month is not None:
            challenges = challenges.filter(
                created__year=int(year),
                created__month=int(month),
            )


        payload = {
            'challenges': []
        }
        for challenge in challenges:
            try:
                p = Post.objects.get(
                    user=request.user,
                    subject=challenge.subject
                )
                post = {
                    'id': p.id,
                    'content': p.content,
                    'image': p.image,
                    'photo': p.photo if p.photo else None
                }
            except Post.DoesNotExist:
                post = None

            payload['challenges'].append({
                'subject': {
                    'id': challenge.subject.id,
                    'title': challenge.subject.title
                },
                'post': post,
                'status': challenge.status.value,
                'created': challenge.created

            })

        return APIResponse({
            'status': 'ok',
            'payload': payload
        })


class ChallengeView(APIView):
    def get(self, request):
        if request.user.is_anonymous:
            return APIResponse({
                'status': 'ok',
                'payload': {
                    'challenge': None
                }
            })

        mychallenge = Challenge.objects.filter(
            user=request.user,
            created__date=datetime.datetime.now().date()
        )

        if mychallenge.exists():
            participant = Challenge.objects.filter(
                subject=mychallenge[0].subject
            ).count()
            achiever = Challenge.objects.filter(
                subject=mychallenge[0].subject,
                status=ChallengeStatus.COMPLETE
            ).count()

            return APIResponse({
                'status': 'ok',
                'payload': {
                    'challenge': {
                        'subject': {
                            'title': mychallenge[0].subject.title
                        },
                        'status': mychallenge[0].status.value,
                        'participant': participant,
                        'achiever': achiever
                    }
                }
            })

        return APIResponse({
            'status': 'ok',
            'payload': {
                'challenge': None
            }
        })

    def post(self, request):
        if not request.user.is_anonymous:
            data = request.data
            user = request.user
            challenge = Challenge(subject_id=data['subject_id'], user=user)
            challenge.save()

            return APIResponse({
                'status': 'ok'
            })

        return HttpResponse('Unauthorized', status=401)


