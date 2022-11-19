# coding: utf-8

from __future__ import unicode_literals

from rest_framework.pagination import PageNumberPagination, \
    LimitOffsetPagination
from django.core.paginator import Paginator as DjangoPaginator


class CustomDjangoPaginator(DjangoPaginator):
    def page(self, number):
        """Return a Page object for the given 1-based page number."""
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page

        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        ids = list(self.object_list.values_list('id', flat=True)[bottom:top])
        return self._get_page(self.object_list.filter(id__in=ids), number, self)


class CustomPageNumberPagination(PageNumberPagination):
    django_paginator_class = CustomDjangoPaginator
    page_size_query_param = 'page_size'
    page_size = 20


class StatPageNumberPagination(PageNumberPagination):
    django_paginator_class = DjangoPaginator
    page_size_query_param = 'page_size'
    page_size = 20
