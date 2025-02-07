from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import UserStatsView, render_user_stats

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'post-tenants', views.PostTenantViewSet)
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'post-landlords', views.PostLandlordViewSet)
router.register(r'followings', views.FollowingsViewSet)
router.register(r'admin-managements', views.AdminManagementViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'image-motels', views.ImageMotelViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Đường dẫn API của router
    path('api/user-stats/', UserStatsView.as_view(), name='user-stats-api'),  # API cho dữ liệu Chart.js
    path('user-stats/', render_user_stats, name='user-stats'),  # Hiển thị trang biểu đồ
]
