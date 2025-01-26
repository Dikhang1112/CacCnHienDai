from rest_framework.serializers import ModelSerializer
from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'user_type', 'avatar', 'phone', 'created_at', 'updated_at', 'active']


