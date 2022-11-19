from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


User = get_user_model()


class BaseModel(models.Model):
    created_time = models.DateTimeField(
        default=timezone.now, verbose_name='创建时间', help_text='创建时间')
    creator = models.ForeignKey(User, on_delete=models.PROTECT,
                                verbose_name='创建人', help_text='创建人',
                                related_name="%(class)s_creator",)
    modified_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    modifier = models.ForeignKey(User, on_delete=models.PROTECT,
                                 verbose_name='修改人', help_text='修改人',
                                 related_name="%(class)s_modifier")
    is_deleted = models.BooleanField(verbose_name='是否已删除', default=False)

    class Meta:
        abstract = True
