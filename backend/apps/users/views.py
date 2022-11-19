import datetime
import time

from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from common.filters import get_search_filter_with_description
from common.permissions import IsSuperUserOrCreator, IsSuperUser
from common.serializers import EmptySerializer
from users.filterset import UserFilterSet
from users.serializers import UserSerializer, ChangePasswordSerializer, \
    RegisterSerializer

User = get_user_model()


@method_decorator(name="list", decorator=swagger_auto_schema(
        operation_summary='获取用户信息',
))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(
        operation_summary='获取单个用户详细信息',
))
@method_decorator(name="create", decorator=swagger_auto_schema(
        operation_summary='创建用户',
))
@method_decorator(name="update", decorator=swagger_auto_schema(
    operation_summary='更新用户信息',
))
@method_decorator(name="partial_update", decorator=swagger_auto_schema(
    operation_summary='更新用户信息',
))
@method_decorator(name="destroy", decorator=swagger_auto_schema(
    operation_summary='删除用户信息',
))
class UserViewSet(viewsets.ModelViewSet):
    """
    用户相关view
    list:
        用户列表(支持模糊查询:username,name)
    retrieve:
        查单个用户详情
    """
    filterset_class = UserFilterSet
    search_fields = ['username', 'nickname', 'email']
    filter_backends = (
        get_search_filter_with_description(search_fields),
        DjangoFilterBackend,
    )

    def get_permissions(self):
        if self.action == 'logout':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'register':
            self.permission_classes = [AllowAny]
        elif self.action in ['destroy', 'update', 'partial_update', 'create']:
            self.permission_classes = [IsSuperUser]
        return super(UserViewSet, self).get_permissions()

    def get_serializer_class(self):
        serializer_map = {
            'logout': EmptySerializer,
            'change_password': ChangePasswordSerializer,
            'register': RegisterSerializer,
            'reset_pwd': EmptySerializer
        }
        return serializer_map.get(self.action, UserSerializer)

    def get_queryset(self):
        if self.request is None:
            return User.objects.none()

        if self.request.user is None:
            return User.objects.none()

        users = User.objects.filter(is_active=True)

        # 用户不是超级用户
        if not self.request.user.is_superuser:
            users = users.filter(id=self.request.user.id)
        return users.order_by('username')

    @swagger_auto_schema(
        method='POST',
        operation_summary='注册用户',
        operation_description='成功返回 200',
        responses={200: None}
    )
    @action(methods=['post'], detail=False)
    def register(self, pk=None):
        """
        游客注册为普通用户
        """
        data = {}
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = User()
        user.username = serializer.validated_data.get('email')
        user.nickname = serializer.validated_data.get('nickname')
        user.email = serializer.validated_data.get('email')
        user.set_password(serializer.validated_data.get('password'))
        user.save()
        data['result'] = 'info'
        data['msg'] = '已注册'
        return Response(data)

    @swagger_auto_schema(
        method='POST',
        operation_summary='修改密码',
        operation_description='成功返回 200',
        responses={200: None}
    )
    @action(methods=['post'], detail=False)
    def change_password(self, pk=None):
        """
        修改密码
        """
        data = {}
        old_password = self.request.data.get('old_password')
        new_password = self.request.data.get('new_password')
        user = self.request.user
        if user.check_password(old_password):
            user.set_password(new_password)
            user.pwd_update_time = datetime.datetime.now()
            user.save()
            data['result'] = 'info'
            data['msg'] = '已修改'
        else:
            data['result'] = 'error'
            data['msg'] = '密码错误，请重新输入'
        return Response(data)

    @swagger_auto_schema(
        method='POST',
        operation_summary='重置密码',
        operation_description='成功返回 200\r\n'
                              '失败（参数错误或不符合要求）返回 400',
        responses={200: None}
    )
    @action(methods=['post'], detail=True)
    def reset_pwd(self, request, pk=None):
        """
        重置密码
        """
        instance = self.get_object()
        instance.set_password('666666')
        instance.pwd_update_time = datetime.datetime.now()
        instance.save()
        return Response({'result': 'info', 'msg': '已重置密码'}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.username = instance.username + "-del%d-" % int(time.time())
        instance.save()

    @swagger_auto_schema(
        method='POST',
        operation_summary='退出登录接口',
        operation_description='成功返回 200',
        responses={200: None}
    )
    @action(methods=['post'], detail=False)
    def logout(self, request, pk=None):
        """
        退出登录
        """
        data = {}
        data['result'] = 'info'
        data['msg'] = '已注销'
        res = Response(data=data)
        res.delete_cookie('token')
        return res
