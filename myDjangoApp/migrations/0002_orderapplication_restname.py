# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myDjangoApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderapplication',
            name='restname',
            field=models.CharField(default='null', max_length=50),
            preserve_default=False,
        ),
    ]
