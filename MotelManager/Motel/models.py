from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')


class UserAccount(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=50, choices=[('type1', 'Type 1'), ('type2', 'Type 2')])


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


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, choices=[
        ('individual', 'Individual'),
        ('company', 'Company'),
    ])

    def __str__(self):
        return f"Admin {self.id} - Type: {self.type}"


class LandLord(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, choices=[
        ('individual', 'Individual'),
        ('company', 'Company'),
    ])

    def to_string_representation(self):
        return f"Landlord {self.id} - Type: {self.type}"


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
