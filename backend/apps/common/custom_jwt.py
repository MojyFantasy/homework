import datetime

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from users.serializers import UserSerializer


User = get_user_model()


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data,
    }


class CustomJSONWebTokenAuthentication(JSONWebTokenAuthentication):
    """
    自定义JWT认证类
    """
    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        username = payload.get('username')

        if not username:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(username=username)
        except:
            msg = _('登录过期，请重新登录')
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _('用户名不存在或被禁用.')
            raise exceptions.AuthenticationFailed(msg)

        return user
