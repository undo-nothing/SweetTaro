from django.contrib.auth.models import Permission
from rest_framework import serializers


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']


class PermissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']


class PermissionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']
