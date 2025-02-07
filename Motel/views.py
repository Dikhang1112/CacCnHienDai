from django.http import HttpResponse
from rest_framework import viewsets, permissions, parsers, generics, status
from . import serializers
from .models import User, Post_Tenant, Comment, Post_Landlord, Followings, AdminManagement, \
    Notification, ImageMotel
from .serializers import UserSerializer, PostTenantSerializer, CommentSerializer, \
    PostLandlordSerializer, FollowingsSerializer, AdminManagementSerializer, \
    NotificationSerializer, ImageMotelSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserStatsSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.exceptions import ValidationError
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveAPIView, generics.ListAPIView):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action.__eq__('current-user'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], url_path='current-user', detail=False)
    def get_current_user(self, request):
        if request.user.is_authenticated:
            user_data = UserSerializer(request.user).data
            return Response(user_data)
        else:
            return Response({"detail": "Authentication credentials were not provided."}, status=401)


class PostTenantViewSet(viewsets.ModelViewSet):
    queryset = Post_Tenant.objects.filter(active=True)
    serializer_class = PostTenantSerializer

    def get_queryset(self):
        return Post_Tenant.objects.filter(active=True).select_related('tenant')

    def perform_create(self, serializer):
        tenant_username = self.request.data.get('tenant')
        tenant = User.objects.filter(username=tenant_username).first()
        if tenant:
            serializer.save(tenant=tenant)
        else:
            raise serializers.ValidationError("Tenant not found.")


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_landlord = self.request.query_params.get('post_landlord', None)
        post_tenant = self.request.query_params.get('post_tenant', None)

        if post_landlord:
            return Comment.objects.filter(post_landlord=post_landlord)
        elif post_tenant:
            return Comment.objects.filter(post_tenant=post_tenant)
        return Comment.objects.none()


class PostLandlordViewSet(viewsets.ModelViewSet):
    queryset = Post_Landlord.objects.filter(active=True)
    serializer_class = PostLandlordSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        user = self.request.user
        if not user:
            raise ValidationError("User is required.")
        return serializer.save(user=user)


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
    parser_classes = [MultiPartParser, FormParser]


class UserStatsView(APIView):
    def get(self, request):
        user_type = request.query_params.get('user_type')
        month = request.query_params.get('month')

        if not user_type:
            return Response({"error": "Missing user_type"}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(user_type=user_type)
        if month:
            users = users.filter(created_at__month=month)

        monthly_counts = users.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id'))

        labels = [f"Month {item['month']}" for item in monthly_counts]
        data = [item['count'] for item in monthly_counts]

        return Response({"labels": labels, "data": data})


class PostStatsView(APIView):
    def get(self, request):
        post_type = request.query_params.get('post_type')
        month = request.query_params.get('month')

        if post_type not in ['tenant', 'landlord']:
            return Response({"error": "Invalid post_type"}, status=status.HTTP_400_BAD_REQUEST)

        if post_type == 'tenant':
            posts = Post_Tenant.objects.filter(active=True)
        else:
            posts = Post_Landlord.objects.filter(active=True)

        if month:
            posts = posts.filter(created_at__month=month)

        monthly_counts = posts.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id'))

        labels = [f"Month {item['month']}" for item in monthly_counts]
        data = [item['count'] for item in monthly_counts]

        return Response({"labels": labels, "data": data})


class IndexView(APIView):
    def get(self, request):
        return HttpResponse("Motel app")


def render_user_stats(request):
    return render(request, 'user_stats.html')
