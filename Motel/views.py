from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(active=True)
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]


def index(request):
    return HttpResponse("Motel app")
