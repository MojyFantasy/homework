# Generated by Django 3.2.10 on 2022-11-20 13:10

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resources', '0002_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='resourcelimit',
            unique_together={('is_deleted', 'user')},
        ),
    ]