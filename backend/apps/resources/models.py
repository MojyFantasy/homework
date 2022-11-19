from django.contrib.auth import get_user_model
from django.db import models

from common.models import BaseModel


User = get_user_model()


class Resource(BaseModel):
    """
    用户资源
    """
    title = models.CharField(verbose_name='标题', help_text='标题', max_length=100)
    content = models.TextField(verbose_name='内容', help_text='内容')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '用户资源'
        verbose_name_plural = verbose_name


class ResourceLimit(BaseModel):
    """
    用户资源配额
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT,
                             verbose_name='配额用户', help_text='配额用户')
    is_limited = models.BooleanField(
        verbose_name='是否配额', help_text='是否配额', default=False)
    max_limit = models.IntegerField(
        verbose_name='配额最大数', help_text='配额最大数')

    class Meta:
        verbose_name = '用户资源配额'
        verbose_name_plural = verbose_name
        unique_together = ['is_deleted', 'user']
