from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'is_staff', 'is_active', 'is_superuser', 'last_login']


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'is_staff', 'is_active', 'is_superuser', 'last_login']
        extra_kwargs = {
            'last_login': {'read_only': True},
        }


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'is_staff', 'is_active', 'is_superuser', 'last_login']
        extra_kwargs = {
            'username': {'read_only': True},
            'last_login': {'read_only': True},
        }
