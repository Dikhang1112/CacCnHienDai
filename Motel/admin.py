from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # Thêm dòng này
from .models import (
    Tenant, Post_Tenant, UserAccount, AdminManagement, Post_Landlord,
    Followings, User, Comment, Notification, ImageMotel
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Thông tin bổ sung', {
            'fields': ('user_type', 'avatar', 'phone'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Thông tin bổ sung', {
            'fields': ('user_type', 'avatar', 'phone'),
        }),
    )

    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'user_type')


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'created_at', 'updated_at', 'active')
    search_fields = ('user__username', 'location')


@admin.register(Post_Tenant)
class PostTenantAdmin(admin.ModelAdmin):
    list_display = ('title', 'tenant', 'created_at', 'updated_at', 'active')
    search_fields = ('title', 'tenant__username')


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'created_at', 'updated_at', 'active')
    search_fields = ('user__username', 'type')
    list_filter = ('type',)


@admin.register(AdminManagement)
class AdminManagementAdmin(admin.ModelAdmin):
    list_display = ('userAccount', 'amount_landlord', 'amount_tenant', 'admin_id', 'post_id')
    search_fields = ('userAccount__user__username', 'admin_id', 'post_id')


@admin.register(Post_Landlord)
class PostLandlordAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'capacity', 'status', 'location', 'created_at', 'updated_at', 'active')
    search_fields = ('title', 'user__username', 'location')
    list_filter = ('status',)


@admin.register(Followings)
class FollowingsAdmin(admin.ModelAdmin):
    list_display = ('user_following', 'user_follower', 'date', 'active')
    search_fields = ('user_following__username', 'user_follower__username')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'post', 'created_at', 'updated_at', 'active')
    search_fields = ('content', 'user__username', 'post__title')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'receiver', 'sender', 'post', 'is_read', 'created_at', 'updated_at', 'active')
    search_fields = ('title', 'receiver__username', 'sender__username', 'post__title')
    list_filter = ('is_read',)


@admin.register(ImageMotel)
class ImageMotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'landlord_id', 'url')
    search_fields = ('landlord_id', 'url')
