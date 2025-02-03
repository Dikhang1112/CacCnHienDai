from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, parsers, generics
from .models import User, Tenant, Post_Tenant, Comment, Post_Landlord, Followings, UserAccount, AdminManagement, \
    Notification, ImageMotel
from .serializers import UserSerializer, TenantSerializer, PostTenantSerializer, CommentSerializer, \
    PostLandlordSerializer, FollowingsSerializer, UserAccountSerializer, AdminManagementSerializer, \
    NotificationSerializer, ImageMotelSerializer
from rest_framework.parsers import MultiPartParser


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveAPIView, generics.ListAPIView):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, ]
    # parser_classes = [parsers.MultiPartParser]


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.filter(active=True)
    serializer_class = TenantSerializer


class PostTenantViewSet(viewsets.ModelViewSet):
    queryset = Post_Tenant.objects.filter(active=True)
    serializer_class = PostTenantSerializer

    def get_queryset(self):
        return Post_Tenant.objects.filter(active=True).select_related('tenant')

    def perform_create(self, serializer):
        serializer.save()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CommentSerializer


class PostLandlordViewSet(viewsets.ModelViewSet):
    queryset = Post_Landlord.objects.filter(active=True)
    serializer_class = PostLandlordSerializer

    def get_queryset(self):
        return Post_Landlord.objects.filter(active=True).select_related('user').prefetch_related('interactions')

    def perform_create(self, serializer):
        serializer.save()


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
    queryset = ImageMotel.objects.all()
    serializer_class = ImageMotelSerializer
    parser_classes = [MultiPartParser, ]


def index(request):
    return HttpResponse("Motel app")
