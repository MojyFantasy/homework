from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


User = get_user_model()


class Command(BaseCommand):
    """
    项目初始化命令: python manage.py init
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # 创建超级用户
        user, _ = User.objects.update_or_create(defaults={
            'email': 'admin@163.com', 'nickname': '管理员',
            'is_superuser': True, 'is_staff': True,
        }, username='admin',)
        user.set_password('admin')
        user.save()

        # 创建超级用户
        user2, _ = User.objects.update_or_create(defaults={
            'email': 'test_user@163.com', 'nickname': '游客1'
        }, username='test_user',)
        user2.set_password('test_user')
        user2.save()
        print("初始化数据完成！")
