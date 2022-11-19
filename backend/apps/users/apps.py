from django.apps import AppConfig


class UsersAppConfig(AppConfig):

    name = "用户相关"
    verbose_name = name

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass
