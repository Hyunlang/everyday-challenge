from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from enumfields import EnumField
from .enums import *


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    date = models.DateField(null=True, default=None)

    class Meta:
        pass

    def get_participant_count(self):
        return Challenge.objects.filter(
            subject=self
        ).filter(
            Q(status=ChallengeStatus.PENDING) |
            Q(status=ChallengeStatus.COMPLETE)
        ).count()

    def get_complete_count(self):
        return Challenge.objects.filter(
            subject=self,
            status=ChallengeStatus.COMPLETE
        ).count()


class Challenge(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    status = EnumField(enum=ChallengeStatus, default=ChallengeStatus.PENDING, max_length=16)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        pass


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    image = models.CharField(max_length=500)
    photo = models.ImageField(upload_to='post/%Y/%m/%d/', null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    def get_like_count(self):
        return Like.objects.filter(post=self).count()

    def get_comments(self):
        return Comment.objects.filter(post=self)


class Like(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        pass


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(default='', max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass
