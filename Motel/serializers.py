from rest_framework.serializers import ModelSerializer, StringRelatedField, IntegerField
from .models import User, Tenant, Post_Tenant, Comment, Post_Landlord, Followings, UserAccount, AdminManagement, \
    Notification, ImageMotel


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'user_type', 'phone', 'created_at', 'updated_at', 'active', 'avatar', 'first_name',
                  'last_name', 'email', 'username', 'password']


class TenantSerializer(ModelSerializer):
    user = StringRelatedField()  # Hiển thị chi tiết thông tin User thay vì ID

    class Meta:
        model = Tenant
        fields = ['id', 'user', 'location', 'created_at', 'updated_at', 'active']


class PostTenantSerializer(ModelSerializer):
    tenant = StringRelatedField()  # Hiển thị chi tiết thông tin Tenant thay vì ID
    comment = StringRelatedField()  # Hiển thị chi tiết thông tin Comment thay vì ID

    class Meta:
        model = Post_Tenant
        fields = ['id', 'tenant', 'comment', 'title', 'content', 'created_at', 'updated_at', 'active']


class CommentSerializer(ModelSerializer):
    user = StringRelatedField()  # Hiển thị chi tiết thông tin User thay vì ID
    post = StringRelatedField()  # Hiển thị chi tiết thông tin PostTenant thay vì ID

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'post', 'created_at', 'updated_at', 'active']


class PostLandlordSerializer(ModelSerializer):
    user = StringRelatedField()  # Hiển thị chi tiết thông tin User thay vì ID

    class Meta:
        model = Post_Landlord
        fields = ['id', 'user', 'title', 'address', 'description', 'price', 'capacity', 'status', 'location',
                  'created_at', 'updated_at', 'active']


class FollowingsSerializer(ModelSerializer):
    user_following = StringRelatedField()  # Hiển thị chi tiết thông tin User (người theo dõi)
    user_follower = StringRelatedField()  # Hiển thị chi tiết thông tin User (người bị theo dõi)

    class Meta:
        model = Followings
        fields = ['id', 'user_following', 'user_follower', 'date', 'created_at', 'updated_at', 'active']


class UserAccountSerializer(ModelSerializer):
    user = StringRelatedField()  # Hiển thị chi tiết thông tin User thay vì ID

    class Meta:
        model = UserAccount
        fields = ['id', 'user', 'type', 'created_at', 'updated_at', 'active']


class AdminManagementSerializer(ModelSerializer):
    userAccount = StringRelatedField()  # Hiển thị chi tiết thông tin UserAccount thay vì ID

    class Meta:
        model = AdminManagement
        fields = ['id', 'userAccount', 'amount_landlord', 'amount_tenant', 'admin_id', 'post_id', 'created_at',
                  'updated_at', 'active']


class NotificationSerializer(ModelSerializer):
    receiver = StringRelatedField()  # Hiển thị chi tiết thông tin User (người nhận thông báo)
    sender = StringRelatedField()  # Hiển thị chi tiết thông tin User (người gửi thông báo)
    post = StringRelatedField()  # Hiển thị chi tiết thông tin Post_Tenant thay vì ID

    class Meta:
        model = Notification
        fields = ['id', 'title', 'content', 'receiver', 'sender', 'post', 'is_read', 'created_at', 'updated_at',
                  'active']


class ImageMotelSerializer(ModelSerializer):
    class Meta:
        model = ImageMotel
        fields = ['id', 'landlord_id', 'url', 'created_at', 'updated_at', 'active']
