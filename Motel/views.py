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
from rest_framework.decorators import action
from rest_framework import serializers


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.filter(is_active=True).all()
#     serializer_class = UserSerializer
#     # permission_classes = [permissions.IsAuthenticated]
#     parser_classes = [MultiPartParser, ]
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveAPIView, generics.ListAPIView):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action == 'current-user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path='current-user', detail=False)
    def get_current_user(self, request):
        return Response(UserSerializer(request.user).data)


class PostTenantViewSet(viewsets.ModelViewSet):
    queryset = Post_Tenant.objects.filter(active=True)
    serializer_class = PostTenantSerializer

    def get_queryset(self):
        return Post_Tenant.objects.filter(active=True).select_related('tenant')

    def perform_create(self, serializer):
        tenant_username = self.request.data.get('tenant')  # Lấy tên người dùng từ request

        # Kiểm tra xem username có tồn tại trong hệ thống không
        tenant = User.objects.filter(username=tenant_username).first()
        if tenant:
            # Gán tenant vào bài đăng
            serializer.save(tenant=tenant)
        else:
            # Nếu không tìm thấy tenant, trả về lỗi
            raise serializers.ValidationError("Tenant not found.")


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        # Lọc bình luận dựa trên post_landlord hoặc post_tenant
        post_landlord = self.request.query_params.get('post_landlord', None)
        post_tenant = self.request.query_params.get('post_tenant', None)

        if post_landlord:
            queryset = Comment.objects.filter(post_landlord=post_landlord)
        elif post_tenant:
            queryset = Comment.objects.filter(post_tenant=post_tenant)
        else:
            queryset = Comment.objects.none()

        return queryset


class PostLandlordViewSet(viewsets.ModelViewSet):
    queryset = Post_Landlord.objects.filter(active=True)
    serializer_class = PostLandlordSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        user = self.request.user
        if not user:
            raise ValidationError("User is required.")

        post_landlord = serializer.save(user=user)
        return post_landlord


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
        # Lọc user theo type hoặc theo tháng
        user_type = request.query_params.get('user_type')
        month = request.query_params.get('month')

        if not user_type or not month:
            return Response({"error": "Missing user_type or month"}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(user_type=user_type, created_at__month=month)

        # Đếm số lượng người dùng
        count = users.count()

        # Tạo dữ liệu
        stats = {
            "user_type": user_type,
            "month": int(month),
            "count": count
        }

        serializer = UserStatsSerializer(stats)
        return Response(serializer.data)
