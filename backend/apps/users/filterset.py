from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from django_filters.rest_framework import FilterSet


User = get_user_model()


class UserFilterSet(FilterSet):

    class Meta:
        model = User
        fields = ['username', ]
