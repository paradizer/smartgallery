# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-16 21:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_auto_20170116_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='imgfile',
            field=models.ImageField(upload_to='images/%Y/%m/%d'),
        ),
    ]
