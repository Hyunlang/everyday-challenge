import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class SignupView(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.create_user(username=data['username'], password=data['password'])
        user.save()

        token = Token.objects.create(user=user)
        return Response({"Token": token.key})


class LoginView(APIView):
    def post(self, request):
        data = request.data
        user = authenticate(username=data['username'], password=data['password'])

        if user is not None:
            token = Token.objects.get(user=user)
            return Response({"Token": token.key, "username": user.username})
        else:
            return Response(data={"error": "Invalid login data"}, status=401)