# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-16 22:26
from __future__ import unicode_literals

from django.db import migrations, models
import gallery.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_auto_20170116_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='imgfile',
            field=models.FileField(upload_to=gallery.models.user_directory_path),
        ),
    ]