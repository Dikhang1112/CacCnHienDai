from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'post-tenants', views.PostTenantViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'post-landlords', views.PostLandlordViewSet)
router.register(r'followings', views.FollowingsViewSet)
router.register(r'user-accounts', views.UserAccountViewSet)
router.register(r'admin-managements', views.AdminManagementViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'image-motels', views.ImageMotelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
