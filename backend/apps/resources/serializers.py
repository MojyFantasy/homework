from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.serializers import BaseModelSerializer
from resources.models import Resource, ResourceLimit
from users.serializers import UserSerializer

User = get_user_model()


class ResourceSerializer(BaseModelSerializer):
    """
    资源 serializer
    """

    class Meta:
        model = Resource
        read_only_fields = ['created_time', 'modified_time', 'creator',
                            'modifier']
        exclude = ['is_deleted']


class ResourceLimitSerializer(BaseModelSerializer):
    """
    用户资源配额 serializer
    """
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True), source='user',
        label='配额用户id', help_text='配额用户id')

    class Meta:
        model = ResourceLimit
        read_only_fields = ['created_time', 'modified_time', 'creator',
                            'modifier']
        exclude = ['is_deleted']
