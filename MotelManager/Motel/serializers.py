from rest_framework import serializers
from .models import User, Tenant, Post, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'avatar', 'phone']


class TenantSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Tenant
        fields = ['id', 'user', 'location', 'created_at', 'updated_at', 'active']


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'user', 'created_at', 'updated_at', 'active']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    post = PostSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'post', 'created_at', 'updated_at', 'active']
