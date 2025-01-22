from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        abstract = True


class User(AbstractUser):
    TENANT = 'tenant'
    LANDLORD = 'landlord'
    USERTYPE_CHOICES = [
        (TENANT, 'Tenant'),
        (LANDLORD, 'Landlord'),
    ]
    user_type = models.CharField(max_length=10,choices=USERTYPE_CHOICES)
    avatar = models.ImageField(upload_to='uploads/%Y/%m')
    phone = models.CharField(max_length=15, blank=True, null=True)
    def __str__(self):
        return f"{self.username} ({self.get_usertype_display()})"


class Tenant(BaseModel):
    user = models.OneToOneField(User, related_name='tenant_account', on_delete=models.CASCADE)
    location = models.TextField(blank=True, null=True)  # Thêm thông tin về địa điểm cho tenant
    def __str__(self):
        return f"{self.user.username} - {self.location}"


class Post(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/%Y/%m', null=True, blank=True)
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Comment(BaseModel):
    content = models.TextField()  # Nội dung bình luận
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)  # Người dùng tạo bình luận
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)  # Bài viết mà bình luận thuộc về
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')
    def __str__(self):
        return self.username


class UserAccount(models.Model):
    """Thông tin chi tiết UserAccount """
    TYPE_CHOICES = [
        ('tenant', 'Tenant'),
        ('landlord', 'Landlord'),
    ]
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='account')  # One-to-one với User
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)  # Enum
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

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


class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    userAccount = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    massage = models.TextField()
    is_read = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    def to_string_representation(self):
        return f"Notifications {self.notification_id}"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    motel_id = models.IntegerField()
    user_id = models.CharField(max_length=255)
    content = models.TextField()  # nội dung khi bình luận
    create_date = models.DateField(auto_now_add=True)

    def to_string_representation(self):
        return f"Comment {self.id} by User {self.user_id}"


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user_type = models.CharField(max_length=50, choices=[
        ('type1', 'Type 1'),
        ('type2', 'Type 2')
    ])
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()  # Nội dung của bài đăng
    title = models.CharField(max_length=255)  # Tiêu đề

    def to_string_representation(self):
        return self.title


class Tennat(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, choices=[
        ('individual', 'Individual'),
        ('company', 'Company'),
    ])

    def to_string_representation(self):
        return f"Tennat {self.id} - Type: {self.type}"


class ImageMotel(models.Model):
    id = models.AutoField(primary_key=True)
    landlord_id = models.IntegerField()
    url = models.URLField(max_length=500)

    def to_string_representation(self):
        return f"Image {self.id} - Landlord {self.landlord_id}"


class Motel(models.Model):
    id = models.AutoField(primary_key=True)
    landlord_id = models.IntegerField()
    title = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    price = models.FloatField()
    capacity = models.IntegerField()  # Giới hạn, sức chứa
    status = models.BooleanField(default=True)  # Trạng thái
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    admin_id = models.IntegerField(null=True, blank=True)

    def to_string_representation(self):
        return self.title


