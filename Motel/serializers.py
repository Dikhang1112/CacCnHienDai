from rest_framework.serializers import ModelSerializer, StringRelatedField, SerializerMethodField, \
    PrimaryKeyRelatedField
from cloudinary.models import CloudinaryField
from .models import User, Post_Tenant, Comment, Post_Landlord, Followings, AdminManagement, \
    Notification, ImageMotel
from rest_framework.fields import CharField, IntegerField
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model


class UserSerializer(ModelSerializer):
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['id', 'user_type', 'phone', 'created_at', 'updated_at', 'active', 'avatar', 'first_name',
                  'last_name', 'email', 'username', 'password']

    def get_avatar(self, obj):
        return obj.avatar.url if obj.avatar else None #tránh lỗi khi avatar rỗng


class PostTenantSerializer(ModelSerializer):
    tenant = StringRelatedField()
    comment = StringRelatedField()

    class Meta:
        model = Post_Tenant
        fields = ['id', 'tenant', 'comment', 'title', 'content', 'price', 'location', 'interaction_type',
                  'created_at', 'updated_at', 'active']


class CommentSerializer(ModelSerializer):
    user = StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'post_tenant', 'post_landlord', 'created_at', 'updated_at', 'active']


class PostLandlordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    # thu cong tung truong anh rieng biet
    image_1 = serializers.ImageField(write_only=True, required=True)
    image_2 = serializers.ImageField(write_only=True, required=True)
    image_3 = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model = Post_Landlord
        fields = ['id', 'user', 'title', 'address', 'description', 'price', 'capacity', 'status', 'location',
                  'interaction_type', 'image_1', 'image_2', 'image_3', 'created_at', 'updated_at', 'active']

    def create(self, validated_data):
        image_1 = validated_data.pop('image_1')
        image_2 = validated_data.pop('image_2')
        image_3 = validated_data.pop('image_3')

        post_landlord = Post_Landlord.objects.create(**validated_data)

        # Lưu ảnh vào ImageMotel
        ImageMotel.objects.create(post_landlord=post_landlord, image=image_1)
        ImageMotel.objects.create(post_landlord=post_landlord, image=image_2)
        ImageMotel.objects.create(post_landlord=post_landlord, image=image_3)

        return post_landlord


class FollowingsSerializer(ModelSerializer):
    user_following = PrimaryKeyRelatedField(queryset=User.objects.all())  # truyen id của following
    user_follower = PrimaryKeyRelatedField(queryset=User.objects.all())  # truyen id cua follower

    class Meta:
        model = Followings
        fields = ['id', 'user_following', 'user_follower', 'date', 'created_at', 'updated_at', 'active']


class AdminManagementSerializer(ModelSerializer):
    userAccount = StringRelatedField()  # Hiển thị tên UserAccount thay vì ID

    class Meta:
        model = AdminManagement
        fields = ['id', 'userAccount', 'amount_landlord', 'amount_tenant', 'admin_id', 'post_id', 'created_at',
                  'updated_at', 'active']


class NotificationSerializer(ModelSerializer):
    receiver = PrimaryKeyRelatedField(queryset=User.objects.all())  # truyen id user
    sender = PrimaryKeyRelatedField(queryset=User.objects.all())
    post = PrimaryKeyRelatedField(queryset=Post_Tenant.objects.all())  # truyen id post_tenant

    class Meta:
        model = Notification
        fields = ['id', 'title', 'content', 'receiver', 'sender', 'post', 'is_read', 'created_at', 'updated_at',
                  'active']


class ImageMotelSerializer(ModelSerializer):
    image_url = SerializerMethodField()

    class Meta:
        model = ImageMotel
        fields = ['id', 'post_landlord', 'image_url', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url  # Lấy URL của ảnh từ Cloudinary
        return None


class UserStatsSerializer(serializers.Serializer):
    user_type = CharField()  # nguoi thue tro hoac chu tro
    month = IntegerField()
    count = IntegerField()
