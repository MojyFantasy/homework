from __future__ import unicode_literals

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    @summary: 用户表的序列化类
    @author: sjh
    """
    password = serializers.CharField(
        help_text='密码', write_only=True, style={'input_type': 'password'})

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'email', 'password')


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    用于修改密码的Serializer
    """
    old_password = serializers.CharField(help_text='原密码', write_only=True)
    new_password = serializers.CharField(help_text='新密码', write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', )


class RegisterSerializer(serializers.ModelSerializer):
    """
    游客注册Serializer
    """
    password = serializers.CharField(
        help_text='密码', write_only=True, style={'input_type': 'password'})

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("该邮箱已被注册！")
        return value

    class Meta:
        model = User
        fields = ('email', 'nickname', 'password', )
