from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True  # lop truu tuong


class User(AbstractUser):
    avatar = CloudinaryField('avatar')
    TENANT = 'tenant'
    LANDLORD = 'landlord'
    USERTYPE_CHOICES = [
        (TENANT, 'Tenant'),
        (LANDLORD, 'Landlord'),
    ]
    user_type = models.CharField(max_length=10, choices=USERTYPE_CHOICES, default=TENANT)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

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
    location = models.TextField(blank=True, null=True)  # Dia chi tenant

    def __str__(self):
        return f"{self.user.username} - {self.location}"


class Post_Tenant(BaseModel):
    tenant = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)  # lien ket voi user
    title = models.CharField(max_length=255)
    content = models.TextField()
    price = models.FloatField(default=0.0)
    LIKE = 'like'
    # DISLIKE = 'dislike'
    # REPORT = 'report'
    VIEW = 'view'

    INTERACTION_CHOICES = [
        (LIKE, 'Like'),
        # (DISLIKE, 'Dislike'),
        # (REPORT, 'Report'),
        (VIEW, 'View'),
    ]

    interaction_type = models.CharField(max_length=10, choices=INTERACTION_CHOICES, default=VIEW)

    class Meta:
        db_table = 'Post_Tenant'

    def __str__(self):
        return self.title


class Comment(BaseModel):
    content = models.TextField()  # noi dung cua comment
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)  # user binh luan
    post = models.ForeignKey('Post_Tenant', related_name='comments',
                             on_delete=models.CASCADE)  # bai viet nguoi dung binh luan

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"


class UserAccount(BaseModel):  # Thừa kế BaseModel
    """Thông tin chi tiết UserAccount """
    TYPE_CHOICES = [
        ('tenant', 'Tenant'),
        ('landlord', 'Landlord'),
    ]
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='account')  # 1-to-1 voi user
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
    receiver = models.ForeignKey('User', on_delete=models.CASCADE, related_name='received_notifications')
    sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sent_notifications')
    post = models.ForeignKey('Post_Tenant', on_delete=models.CASCADE, related_name='notifications',
                             related_query_name='notification')
    is_read = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'notification'


class ImageMotel(models.Model):
    id = models.AutoField(primary_key=True)
    post_landlord = models.ForeignKey(
        'Post_Landlord',
        on_delete=models.CASCADE,
        related_name='images',
        null=True,
        blank=True
    )
    image = CloudinaryField('image', default="https://res.cloudinary.com/demo/image/upload/sample.jpg")

    def __str__(self):
        return f"Image {self.id} - Post {self.post_landlord.title}"


class Post_Landlord(BaseModel):
    user = models.ForeignKey(User, related_name='landlord_posts', on_delete=models.CASCADE)  # lien ket toi user
    title = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    price = models.FloatField()
    capacity = models.IntegerField()
    status = models.BooleanField(default=True)  # trang thai xem bai dang con hieu luc k?
    location = models.CharField(max_length=255, null=True, blank=True)
    INTERACTION_CHOICES = [
        ('like', 'Like'),
        # ('dislike', 'Dislike'),
        # ('report', 'Report'),
        ('view', 'View'),
    ]

    interaction_type = models.CharField(max_length=10, choices=INTERACTION_CHOICES, default='view')

    class Meta:
        db_table = 'Post_Landlord'

    def __str__(self):
        return self.title


class Followings(BaseModel):
    user_following = models.ForeignKey(
        User, related_name='followings', on_delete=models.CASCADE
    )
    user_follower = models.ForeignKey(
        User, related_name='followers', on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True)  # thoi gian follow

    def __str__(self):
        return f"{self.user_following.username} follows {self.user_follower.username}"

    class Meta:
        db_table = 'Followings'
        unique_together = ('user_following', 'user_follower')
