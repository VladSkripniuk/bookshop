# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.ForeignKey(to='app.Category', null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(null=True, upload_to=b'images'),
        ),
        migrations.AlterField(
            model_name='book',
            name='file',
            field=models.FileField(null=True, upload_to=b'books'),
        ),
    ]
