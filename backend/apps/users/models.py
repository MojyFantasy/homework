from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):

    nickname = models.CharField(verbose_name='中文名', max_length=50,
                                default='匿名', help_text='中文名')

    def __str__(self):
        return self.nickname


