from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, parsers, generics, status
from .models import User, Post_Tenant, Comment, Post_Landlord, Followings, AdminManagement, \
    Notification, ImageMotel
from .serializers import UserSerializer, PostTenantSerializer, CommentSerializer, \
    PostLandlordSerializer, FollowingsSerializer, AdminManagementSerializer, \
    NotificationSerializer, ImageMotelSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserStatsSerializer
from django.db import IntegrityError


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, ]


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

    def get_queryset(self):
        # Lọc bình luận chỉ cho bài viết với ID cụ thể
        post_id = self.request.query_params.get('post', None)
        if post_id is not None:
            return Comment.objects.filter(post_id=post_id)
        return Comment.objects.all()  # Hoặc trả về một danh sách rỗng nếu không có post_id


class PostLandlordViewSet(viewsets.ModelViewSet):
    queryset = Post_Landlord.objects.filter(active=True)
    serializer_class = PostLandlordSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post_Landlord.objects.filter(active=True).select_related('user').prefetch_related('interactions')

    def perform_create(self, serializer):
        user = self.request.user
        if not user:
            raise ValidationError("User is required.")
        serializer.save(user=user)


class FollowingsViewSet(viewsets.ModelViewSet):
    queryset = Followings.objects.filter(active=True)
    serializer_class = FollowingsSerializer


class AdminManagementViewSet(viewsets.ModelViewSet):
    queryset = AdminManagement.objects.all()
    serializer_class = AdminManagementSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.filter(active=True)
    serializer_class = NotificationSerializer


class ImageMotelViewSet(viewsets.ModelViewSet):
    queryset = ImageMotel.objects.all()
    serializer_class = ImageMotelSerializer
    parser_classes = [MultiPartParser, FormParser]  # Hỗ trợ upload file


def index(request):
    return HttpResponse("Motel app")


class UserStatsView(APIView):
    def get(self, request):
        # loc user theo type hoac theo thang
        user_type = request.query_params.get('user_type')
        month = request.query_params.get('month')

        if not user_type or not month:
            return Response({"error": "Missing user_type or month"}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(user_type=user_type, created_at__month=month)

        # dem sl nguoi dung
        count = users.count()

        # tao du lieu
        stats = {
            "user_type": user_type,
            "month": int(month),
            "count": count
        }

        serializer = UserStatsSerializer(stats)

        return Response(serializer.data)
