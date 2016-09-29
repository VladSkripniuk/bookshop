# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import app.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20160910_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='number_of_books',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='total_price',
        ),
        migrations.AlterField(
            model_name='cart',
            name='token',
            field=models.CharField(default=app.models.create_token, max_length=40),
        ),
        migrations.RemoveField(
            model_name='purchased',
            name='book',
        ),
        migrations.AddField(
            model_name='purchased',
            name='book',
            field=models.ForeignKey(to='app.Book', null=True),
        ),
        migrations.AlterField(
            model_name='purchased',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
