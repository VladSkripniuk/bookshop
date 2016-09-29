# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20160904_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='archive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cart',
            name='number_of_books',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cart',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cart',
            name='token',
            field=models.CharField(default=b'yKmO64L7D0b6VcTd', max_length=40),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
