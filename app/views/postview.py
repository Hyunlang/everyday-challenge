import json

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from ..models import *
from ..response import APIResponse
import datetime


class PostListView(generics.ListAPIView):
    def get_user(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def list(self, request):
        challenge = Challenge.objects.filter(
            user=self.get_user(request.user.id),
            created__date=datetime.datetime.now().date()
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
