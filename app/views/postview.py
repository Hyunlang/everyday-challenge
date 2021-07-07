import json
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from ..models import *
from ..response import APIResponse
import datetime


class PostListCreateView(generics.ListCreateAPIView):
    def get_user(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def list(self, request):
        subject_id = request.GET.get('subjectId', None)
        if subject_id is not None:
            challenge = Challenge.objects.filter(
                subject__id=subject_id
            )
        else:
            challenge = Challenge.objects.filter(
                created__date=datetime.datetime.now().date()
            )
            if not request.user.is_anonymous:
                challenge = challenge.filter(
                    user=request.user
                )

        if challenge.exists():
            posts = Post.objects.filter(
                subject=challenge[0].subject
            ).order_by('-created')
        else:
            posts = []

        payload = {
            'posts': [{
                'username': post.user.username,
                'subject': {
                    'title': post.subject.title
                },
                'content': post.content,
                'image': post.image,
                'photo': post.photo.url if post.photo else None,
                'like': post.get_like_count(),
                'comments': [{
                    'username': comment.user.username,
                    'content': comment.content,
                    'created': comment.created
                } for comment in post.get_comments()]
            } for post in posts]
        }

        return APIResponse({
            'status': 'ok',
            'payload': payload
        })

    def post(self, request):
        if not request.user.is_anonymous:
            # data = json.loads(request.body)
            data = request.data
            user = request.user
            subject_id = data.get('subject_id', None)
            content = data.get('content', None)
            # image = data.get('image', None)
            photo = data.get('photo', None)

            if subject_id and content and photo:
                post = Post(user=user, subject_id=subject_id, content=content, photo=photo)
                post.save()

                challenge = Challenge.objects.get(user=user, created__date=datetime.date.today())
                challenge.status = 'complete'
                challenge.save()

                return APIResponse({
                    'status': 'ok'
                })
            return HttpResponse('Bad Request', status=400)
        return HttpResponse('Unauthorized', status=401)

class PostView(APIView):
    def get(self, request, id):
        try:
            post = Post.objects.get(id=id)
            payload = {
                'post': {
                    'username': post.user.username,
                    'subject': {
                        'title': post.subject.title
                    },
                    'content': post.content,
                    'image': post.image,
                    'photo': post.photo.url if post.photo else None,
                    'like': post.get_like_count(),
                    'comments': [{
                        'username': comment.user.username,
                        'content': comment.content,
                        'created': comment.created
                    } for comment in post.get_comments()],
                    'created': post.created
                }
            }
            return APIResponse({
                'status': 'ok',
                'payload': payload
            })

        except Post.DoesNotExist:
            return APIResponse({
                'status': 'ok',
                'payload': {
                    'post': None
                }
            })

    def post(self, request):
        pass


class LikeView(APIView):
    def post(self, request, id):
        post = Post.objects.get(id=id)
        Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        return APIResponse({
            'status': 'ok',
            'payload': {
                'post': {
                    'id': post.id,
                    'like': post.get_like_count()
                }
            }
        })


class CommentListView(generics.ListAPIView):
    def list(self, request, id):
        post = Post.objects.get(id=id)
        comments = Comment.objects.filter(
            post=post
        ).order_by('-created')

        payload = [{
            'id': id,
            'username': comment.user.username,
            'content': comment.content,
            'created': comment.created
        } for comment in comments]

        return APIResponse({
            'status': 'ok',
            'payload': payload
        })


class CommentView(APIView):
    def post(self, request, id):
        post = Post.objects.get(id=id)
        Comment.objects.create(
            user=request.user,
            post=post,
            content=request.data['content']
        )

        return APIResponse({
            'status': 'ok',
        })
