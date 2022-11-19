import datetime
import time

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, serializers

from common.filters import get_search_filter_with_description
from common.permissions import IsSuperUserOrCreator, IsSuperUser
from resources.filterset import ResourceFilterSet, ResourceLimitFilterSet
from resources.models import Resource, ResourceLimit
from resources.serializers import ResourceSerializer, ResourceLimitSerializer

User = get_user_model()


@method_decorator(name="list", decorator=swagger_auto_schema(
        operation_summary='获取资源列表',
))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(
        operation_summary='获取单个资源详细信息',
))
@method_decorator(name="create", decorator=swagger_auto_schema(
        operation_summary='创建资源',
))
@method_decorator(name="update", decorator=swagger_auto_schema(
    operation_summary='更新资源信息',
))
@method_decorator(name="partial_update", decorator=swagger_auto_schema(
    operation_summary='更新资源信息',
))
@method_decorator(name="destroy", decorator=swagger_auto_schema(
    operation_summary='删除资源信息',
))
class ResourceViewSet(viewsets.ModelViewSet):
    """
    资源相关view
    list:
        资源列表(支持模糊查询:title,content)
    retrieve:
        查单个资源详情
    """
    filterset_class = ResourceFilterSet
    search_fields = ['title', 'content']
    filter_backends = (
        get_search_filter_with_description(search_fields),
        DjangoFilterBackend,
    )

    serializer_class = ResourceSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update', 'create']:
            self.permission_classes = [IsSuperUserOrCreator]
        return super(ResourceViewSet, self).get_permissions()

    def get_queryset(self):
        if self.request is None:
            return Resource.objects.none()

        if isinstance(self.request.user, AnonymousUser):
            return Resource.objects.none()

        qs = Resource.objects.filter(is_deleted=False)

        return qs.order_by('-created_time')

    def perform_create(self, serializer):
        # 判断当前登录用户是否超配额，如果超配额，则不允许创建
        qs = ResourceLimit.objects.filter(
            user=self.request.user, is_deleted=False, is_limited=True)
        if qs.exists():
            max_limit = qs.first().max_limit
            created_resource_count = Resource.objects.filter(
                is_deleted=False, creator=self.request.user).count()
            if max_limit <= created_resource_count:
                raise serializers.ValidationError(
                    f'您的资源已达到配额数（{max_limit}），无法创建。')

        serializer.save()

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


@method_decorator(name="list", decorator=swagger_auto_schema(
        operation_summary='获取资源配额列表',
))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(
        operation_summary='获取单个资源配额详细信息',
))
@method_decorator(name="create", decorator=swagger_auto_schema(
        operation_summary='创建资源配额',
))
@method_decorator(name="update", decorator=swagger_auto_schema(
    operation_summary='更新资源配额信息',
))
@method_decorator(name="partial_update", decorator=swagger_auto_schema(
    operation_summary='更新资源配额信息',
))
@method_decorator(name="destroy", decorator=swagger_auto_schema(
    operation_summary='删除资源配额信息',
))
class ResourceLimitViewSet(viewsets.ModelViewSet):
    """
    资源配额相关view
    list:
        资源配额列表(支持模糊查询:title,content)
    retrieve:
        查单个资源配额详情
    """
    filterset_class = ResourceLimitFilterSet
    search_fields = []
    filter_backends = (
        get_search_filter_with_description(search_fields),
        DjangoFilterBackend,
    )

    serializer_class = ResourceLimitSerializer
    permission_classes = [IsSuperUser, ]

    def get_queryset(self):
        if self.request is None:
            return ResourceLimit.objects.none()

        if isinstance(self.request.user, AnonymousUser):
            return ResourceLimit.objects.none()

        # 用户不是超级用户
        if not self.request.user.is_superuser:
            return ResourceLimit.objects.none()

        qs = ResourceLimit.objects.filter(is_deleted=False)
        return qs.order_by('-created_time')

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

