from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Post_Landlord, User


@receiver(post_save, sender=Post_Landlord)
def notify_tenants(sender, instance, created, **kwargs):
    """Gửi email đến tất cả Tenant khi có bài đăng mới từ Landlord."""
    if created:  # Chỉ gửi khi bài đăng mới được tạo
        tenant_users = User.objects.filter(user_type='tenant')

        recipient_list = [tenant.email for tenant in tenant_users if tenant.email]

        if recipient_list:  # Kiểm tra có Tenant nào có email không
            send_mail(
                subject=" Có phòng trọ mới được đăng!",
                message=f"Chào bạn, có một bài đăng mới: {instance.title} tại {instance.address} với giá {instance.price}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
