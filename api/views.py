# from django.shortcuts import render
from rest_framework import viewsets

from .serializers import UserSerializer, TrackSerializer
from .models import User, Track


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all().order_by('title')
    serializer_class = TrackSerializer
