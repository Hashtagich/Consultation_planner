from rest_framework import serializers
from users.models import CustomUser, Role
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

CustUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustUser
        fields = (
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'role',
            'password'
        )


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustUser
        fields = (
            'first_name',
            'last_name',
            'middle_name',
            # 'email',
            # 'role',
            'password'
        )


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'title',
        )


class MyUserSerializerForGet(serializers.ModelSerializer):
    role = serializers.CharField(source='role.title', allow_blank=True, default='')

    class Meta:
        model = CustomUser
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
        model = CustomUser
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
