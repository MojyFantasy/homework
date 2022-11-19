from .base import *  # noqa
from .base import env

DEBUG = False

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="hwBQgMRpYrNxrCWdKKNZcgfHYMvMjPDmIv0W3dMyFEAxEV9eS98pUdRN3Kq2mRBt",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
# ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["example.com"])
ALLOWED_HOSTS = ['*', ]
# DATABASES
# ------------------------------------------------------------------------------
# DATABASES["default"] = env.db("DATABASE_URL")  # noqa F405
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': env.str('DATABASE_NAME'),
#         'USER': env.str('DATABASE_USER'),
#         'PASSWORD': env.str('DATABASE_PASSWORD'),
#         'HOST': env.str('DATABASE_HOST'),
#         'PORT': env.str('DATABASE_PORT'),
#         'OPTIONS': {
#             'init_command': 'SET sql_mode=STRICT_TRANS_TABLES',
#         },
#     }
# }

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES[0]["OPTIONS"]["loaders"] = [  # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

# ------------------------------------------------------------------------------
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
   'burst': '1/min',
   'sustained': '30/day',
}
