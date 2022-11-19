from rest_framework import serializers

from common.models import BaseModel
from users.serializers import UserSerializer


class EmptySerializer(serializers.BaseSerializer):
    """
    有时viewset的某个action不需要任何Serializer（如，删除时只需要一个pk），
    为了避免额外的参数在自动生成的api文档中带来困惑，可使用这个空Serializer
    """
    pass


class BaseModelSerializer(serializers.ModelSerializer):
    """
    流程基类 serializer
    """

    creator = UserSerializer(read_only=True)
    creator_id = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), source="creator",
        write_only=True, label="创建人", help_text="创建人")
    modifier = UserSerializer(read_only=True)
    modifier_id = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), source="modifier",
        write_only=True, label="修改人", help_text="修改人")

    class Meta:
        model = BaseModel
        fields = '__all__'
