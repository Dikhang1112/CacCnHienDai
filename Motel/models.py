from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True   # Lớp trừu tượng


class User(AbstractUser):
    TENANT = 'tenant'
    LANDLORD = 'landlord'
    USERTYPE_CHOICES = [
        (TENANT, 'Tenant'),
        (LANDLORD, 'Landlord'),
    ]
    user_type = models.CharField(max_length=10, choices=USERTYPE_CHOICES, default=TENANT)
    avatar = models.ImageField(upload_to='uploads/%Y/%m')
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    # Thêm related_name để tránh xung đột với Django's auth User
    groups = models.ManyToManyField(
        'auth.Group', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', blank=True
    )

    def __str__(self):
        try:
            return f"{self.username} - {self.get_usertype_display()}"
        except AttributeError:
            return f"{self.username} - Unknown"

class Tenant(BaseModel):
    user = models.OneToOneField(User, related_name='tenant_account', on_delete=models.CASCADE)
    location = models.TextField(blank=True, null=True)  # Thêm thông tin về địa điểm cho tenant

    def __str__(self):
        return f"{self.user.username} - {self.location}"


class Post_Tenant(BaseModel):
    tenant = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)  # Liên kết đến User (Tenant)
    comment = models.ForeignKey('Comment', related_name='post_tenant', on_delete=models.SET_NULL, null=True, blank=True)  # Liên kết đến Comment
    title = models.CharField(max_length=255)  # Tiêu đề bài đăng
    content = models.TextField()  # Nội dung bài đăng

    class Meta:
        db_table = 'Post_Tenant'

    def __str__(self):
        return self.title


class Comment(BaseModel):
    content = models.TextField()  # Nội dung bình luận
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)  # Người dùng tạo bình luận
    post = models.ForeignKey('Post_Tenant', related_name='comments', on_delete=models.CASCADE)  # Bài viết mà bình luận thuộc về

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"


class UserAccount(BaseModel):  # Thừa kế BaseModel
    """Thông tin chi tiết UserAccount """
    TYPE_CHOICES = [
        ('tenant', 'Tenant'),
        ('landlord', 'Landlord'),
    ]
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='account')  # One-to-one với User
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)  # Enum

    def __str__(self):
        return f"{self.user.username} - {self.type}"


class AdminManagement(models.Model):
    id = models.AutoField(primary_key=True)
    userAccount = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    amount_landlord = models.IntegerField()
    amount_tenant = models.IntegerField()
    admin_id = models.IntegerField()
    post_id = models.IntegerField()

    def to_string_representation(self):
        return f"UserAccount {self.id}"


class Notification(BaseModel):
    title = models.TextField(null=False)
    content = models.TextField(null=False)
    receiver = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sent_notifications')
    sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='received_notifications')
    post = models.ForeignKey('Post_Tenant', on_delete=models.CASCADE, related_name='notifications', related_query_name='notification')
    is_read = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'notification'


class ImageMotel(models.Model):
    id = models.AutoField(primary_key=True)
    landlord_id = models.IntegerField()
    url = models.URLField(max_length=500)

    def to_string_representation(self):
        return f"Image {self.id} - Landlord {self.landlord_id}"


class Post_Landlord(BaseModel):
    user = models.ForeignKey(User, related_name='landlord_posts', on_delete=models.CASCADE)  # Liên kết tới bảng User
    title = models.CharField(max_length=255)  # Tiêu đề bài viết
    address = models.TextField()  # Địa chỉ
    description = models.TextField()  # Mô tả
    price = models.FloatField()  # Giá tiền
    capacity = models.IntegerField()  # Sức chứa
    status = models.BooleanField(default=True)  # Trạng thái bài đăng (còn hiệu lực hay không)
    location = models.CharField(max_length=255, null=True, blank=True)  # Vị trí

    class Meta:
        db_table = 'Post_Landlord'  # Tên bảng trong cơ sở dữ liệu

    def __str__(self):
        return self.title


class Followings(BaseModel):
    user_following = models.ForeignKey(
        User, related_name='followings', on_delete=models.CASCADE
    )  # Người dùng thực hiện theo dõi
    user_follower = models.ForeignKey(
        User, related_name='followers', on_delete=models.CASCADE
    )  # Người dùng được theo dõi
    date = models.DateTimeField(auto_now_add=True)  # Thời điểm theo dõi

    def __str__(self):
        return f"{self.user_following.username} follows {self.user_follower.username}"

    class Meta:
        db_table = 'Followings'
        unique_together = ('user_following', 'user_follower')  # Đảm bảo một cặp chỉ tồn tại một lần
