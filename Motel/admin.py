from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Tenant, Post_Tenant, UserAccount, AdminManagement, Post_Landlord, Followings, User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Các trường hiển thị trong form sửa và thêm
    fieldsets = UserAdmin.fieldsets + (
        ('Thông tin bổ sung', {
            'fields': ('user_type', 'avatar', 'phone'),
        }),
    )

    # Các trường khi tạo mới người dùng
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Thông tin bổ sung', {
            'fields': ('user_type', 'avatar', 'phone'),
        }),
    )

    # Các trường hiển thị trong danh sách admin
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'user_type')


class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at')
    search_fields = ('name', 'location')


class PostTenantAdmin(admin.ModelAdmin):
    list_display = ('title', 'tenant', 'created_at')
    search_fields = ('title',)


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_type', 'created_at')  # Hiển thị các trường cần thiết
    search_fields = ('user__username', 'account_type')  # Cho phép tìm kiếm
    list_filter = ('account_type',)  # Thêm bộ lọc


class AdminManagementAdmin(admin.ModelAdmin):
    list_display = ('admin_user', 'role', 'created_at')  # Hiển thị thông tin cơ bản
    search_fields = ('admin_user__username', 'role')  # Tìm kiếm theo admin và vai trò
    list_filter = ('role',)  # Bộ lọc theo vai trò


# Register your models here.
admin.site.register(Tenant)
admin.site.register(Post_Tenant)
admin.site.register(UserAccount)
admin.site.register(AdminManagement)
admin.site.register(Post_Landlord)
admin.site.register(Followings)