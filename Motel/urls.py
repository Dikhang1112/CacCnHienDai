from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserStatsView

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
    path('', include(router.urls)),
    path('user-stats/', UserStatsView.as_view(), name='user-stats'),
]
