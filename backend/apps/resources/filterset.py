from django_filters import rest_framework as filters
from django_filters.rest_framework import FilterSet

from resources.models import Resource, ResourceLimit


class ResourceFilterSet(FilterSet):

    class Meta:
        model = Resource
        fields = ['creator', ]


class ResourceLimitFilterSet(FilterSet):

    class Meta:
        model = ResourceLimit
        fields = ['creator', 'user']
