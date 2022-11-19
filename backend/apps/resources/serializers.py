from rest_framework import serializers

from common.serializers import BaseModelSerializer
from resources.models import Resource, ResourceLimit
from users.serializers import UserSerializer


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

    class Meta:
        model = ResourceLimit
        read_only_fields = ['created_time', 'modified_time', 'creator',
                            'modifier']
        exclude = ['is_deleted']
