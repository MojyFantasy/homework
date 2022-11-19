from rest_framework import filters


def get_search_filter_with_description(search_fields):
    class DescribedSearchFilter(filters.SearchFilter):
        fields_str = '、'.join(search_fields)
        search_description = f'空格分隔的多关键字搜索。可搜字段：{fields_str}'
    return DescribedSearchFilter
