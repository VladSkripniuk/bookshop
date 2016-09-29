# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20160830_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='token',
            field=models.CharField(default=b'm6H4C5UnyRLCPHXH', max_length=40),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
