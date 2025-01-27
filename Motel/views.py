from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from .models import User, Tenant, Post_Tenant, Comment, Post_Landlord, Followings, UserAccount, AdminManagement, Notification, ImageMotel
from .serializers import UserSerializer, TenantSerializer, PostTenantSerializer, CommentSerializer, PostLandlordSerializer, FollowingsSerializer, UserAccountSerializer, AdminManagementSerializer, NotificationSerializer, ImageMotelSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(active=True)
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.filter(active=True)
    serializer_class = TenantSerializer


class PostTenantViewSet(viewsets.ModelViewSet):
    queryset = Post_Tenant.objects.filter(active=True)
    serializer_class = PostTenantSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CommentSerializer


class PostLandlordViewSet(viewsets.ModelViewSet):
    queryset = Post_Landlord.objects.filter(active=True)
    serializer_class = PostLandlordSerializer


class FollowingsViewSet(viewsets.ModelViewSet):
    queryset = Followings.objects.filter(active=True)
    serializer_class = FollowingsSerializer


class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.filter(active=True)
    serializer_class = UserAccountSerializer


class AdminManagementViewSet(viewsets.ModelViewSet):
    queryset = AdminManagement.objects.all()
    serializer_class = AdminManagementSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.filter(active=True)
    serializer_class = NotificationSerializer


class ImageMotelViewSet(viewsets.ModelViewSet):
    queryset = ImageMotel.objects.filter(id=True)
    serializer_class = ImageMotelSerializer


def index(request):
    return HttpResponse("Motel app")
