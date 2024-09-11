from rest_framework import serializers
from users.models import User, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'title',
        )


class MyUserSerializerForGet(serializers.ModelSerializer):
    role = serializers.CharField(source='role.title', allow_blank=True, default='')

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'role',
            'phone',
            'email',
            'is_staff',
            'is_active',
            'is_blocked'
        )


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'role',
            'is_staff',
            'is_active',
            'is_blocked'
        )
