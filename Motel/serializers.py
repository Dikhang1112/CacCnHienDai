from rest_framework.serializers import ModelSerializer, StringRelatedField, SerializerMethodField, \
    PrimaryKeyRelatedField
from cloudinary.models import CloudinaryField
from .models import User, Post_Tenant, Comment, Post_Landlord, Followings, AdminManagement, \
    Notification, ImageMotel
from rest_framework.fields import CharField, IntegerField
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'user_type', 'phone', 'created_at', 'updated_at', 'active', 'avatar', 'first_name',
                  'last_name', 'email', 'username', 'password']


class PostTenantSerializer(ModelSerializer):
    tenant = StringRelatedField()
    comment = StringRelatedField()

    class Meta:
        model = Post_Tenant
        fields = ['id', 'tenant', 'comment', 'title', 'content', 'price', 'interaction_type',
                  'created_at', 'updated_at', 'active']


class CommentSerializer(ModelSerializer):
    user = StringRelatedField()
    post = StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'post', 'created_at', 'updated_at', 'active']


class PostLandlordSerializer(ModelSerializer):
    user = StringRelatedField()  # Hiển thị tên User thay vì ID

    class Meta:
        model = Post_Landlord
        fields = ['id', 'user', 'title', 'address', 'description', 'price', 'capacity', 'status', 'location',
                  'interaction_type',  # Thêm interaction_type vào đây
                  'created_at', 'updated_at', 'active']


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
