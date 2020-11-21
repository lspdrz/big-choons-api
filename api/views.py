from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, TrackSerializer
from .models import Track


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer


class TrackViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Track.objects.all().order_by('title')
    serializer_class = TrackSerializer


class GoogleAuthView(APIView):
    def post(self, request):
        payload = {'access_token': request.data.get(
            "token")
        }  # validate the token
        r = requests.get(
            'https://www.googleapis.com/oauth2/v2/userinfo', params=payload
        )
        data = json.loads(r.text)

        if 'error' in data:
            content = {
                'message': 'wrong google token / this google token is already expired.'
            }
            return Response(content)

        # create user if they don't exist
        print('hello google data')
        print(data)
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            user = User()
            user.username = data['email']
            user.first_name = data['given_name']
            user.last_name = data['family_name']
            # provide random default password
            user.password = make_password(
                BaseUserManager().make_random_password()
            )
            user.email = data['email']
            user.save()

        # generate token without username & password
        token = RefreshToken.for_user(user)
        response = {}
        response['id'] = user.pk
        response['username'] = user.username
        response['name'] = user.first_name + " " + user.last_name
        response['email'] = user.email
        response['access_token'] = str(token.access_token)
        response['refresh_token'] = str(token)
        return Response(response)
