from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.tokens import RefreshToken

import requests
from .serializers import UserSerializer, TrackSerializer, TokenObtainExpirySerializer
from .models import Track


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer


class TrackViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Track.objects.all().order_by('title')
    serializer_class = TrackSerializer


class TokenObtainPairView(TokenViewBase):
    """
        Return JWT tokens (access and refresh) for specific user based on username and password.
    """
    serializer_class = TokenObtainExpirySerializer


class TokenRefreshView(TokenViewBase):
    """
        Renew tokens (access and refresh) with new expire time based on specific user's access token.
    """

    def get(self, request):
        print("hello")
        print(request.COOKIES)
        try:
            refresh_token = request.COOKIES['refresh_token']
            if refresh_token:
                response = Response()
                token = RefreshToken(refresh_token)
                response.set_cookie(key='refresh_token',
                                    value=str(token), httponly=True)
                response.data = {
                    'access_token': str(token.access_token),
                    'access_token_expiry': str(
                        token.access_token.payload['exp']),
                }
                return response
            else:
                raise ValidationError('No Refresh Token Available')
        except:
            raise ValidationError('No Refresh Token Available')


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
        response = Response()
        response.set_cookie(key='refresh_token',
                            value=str(token), httponly=True)
        response.data = {
            'id': user.pk,
            'username': user.username,
            'name': user.first_name + " " + user.last_name,
            'email': user.email,
            'access_token': str(token.access_token),
            'access_token_expiry': str(
                token.access_token.payload['exp']),
        }
        return response
