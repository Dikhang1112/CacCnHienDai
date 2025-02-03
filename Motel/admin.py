from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # Thêm dòng này
from .models import (
    Post_Tenant, UserAccount, AdminManagement, Post_Landlord,
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
    list_display = ('content', 'user', 'get_post_tenant_title', 'get_post_landlord_title')

    def get_post_tenant_title(self, obj):
        return obj.post_tenant.title if obj.post_tenant else None  # Trả về tiêu đề của post_tenant nếu có
    get_post_tenant_title.admin_order_field = 'post_tenant__title'  # Cho phép sắp xếp theo title của post_tenant
    get_post_tenant_title.short_description = 'Post Tenant Title'  # Tên cột trong trang admin

    def get_post_landlord_title(self, obj):
        return obj.post_landlord.title if obj.post_landlord else None  # Trả về tiêu đề của post_landlord nếu có
    get_post_landlord_title.admin_order_field = 'post_landlord__title'  # Cho phép sắp xếp theo title của post_landlord
    get_post_landlord_title.short_description = 'Post Landlord Title'  # Tên cột trong trang admin



@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'receiver', 'sender', 'post', 'is_read', 'created_at', 'updated_at', 'active')
    search_fields = ('title', 'receiver__username', 'sender__username', 'post__title')
    list_filter = ('is_read',)


@admin.register(ImageMotel)
class ImageMotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_landlord', 'image')
    search_fields = ('post_landlord__title',)
