from rest_framework.serializers import ModelSerializer, StringRelatedField
from cloudinary.models import CloudinaryField
from .models import User, Post_Tenant, Comment, Post_Landlord, Followings, UserAccount, AdminManagement, \
    Notification, ImageMotel


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
        fields = ['id', 'tenant', 'comment', 'title', 'content', 'price', 'interaction_type',  # Thêm các trường mới
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
    user_following = StringRelatedField()  # Hiển thị tên User (người theo dõi)
    user_follower = StringRelatedField()  # Hiển thị tên User (người bị theo dõi)

    class Meta:
        model = Followings
        fields = ['id', 'user_following', 'user_follower', 'date', 'created_at', 'updated_at', 'active']


class UserAccountSerializer(ModelSerializer):
    user = StringRelatedField()  # Hiển thị tên User thay vì ID

    class Meta:
        model = UserAccount
        fields = ['id', 'user', 'type', 'created_at', 'updated_at', 'active']


class AdminManagementSerializer(ModelSerializer):
    userAccount = StringRelatedField()  # Hiển thị tên UserAccount thay vì ID

    class Meta:
        model = AdminManagement
        fields = ['id', 'userAccount', 'amount_landlord', 'amount_tenant', 'admin_id', 'post_id', 'created_at',
                  'updated_at', 'active']


class NotificationSerializer(ModelSerializer):
    receiver = StringRelatedField()  # Hiển thị tên User (người nhận thông báo)
    sender = StringRelatedField()  # Hiển thị tên User (người gửi thông báo)
    post = StringRelatedField()  # Hiển thị tên Post_Tenant thay vì ID

    class Meta:
        model = Notification
        fields = ['id', 'title', 'content', 'receiver', 'sender', 'post', 'is_read', 'created_at', 'updated_at',
                  'active']


class ImageMotelSerializer(ModelSerializer):
    image = CloudinaryField()

    class Meta:
        model = ImageMotel
        fields = ['id', 'post_landlord', 'url', 'created_at', 'updated_at', 'active']
