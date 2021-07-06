from django.db import models
from enumfields import EnumField
from .enums import *
from django.contrib.auth.models import User


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    date = models.DateField(null=True, default=None)

    class Meta:
        pass


class Challenge(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    status = EnumField(enum=ChallengeStatus, max_length=16)
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
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass


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
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass
