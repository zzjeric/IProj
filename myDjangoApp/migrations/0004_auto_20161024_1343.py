# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 13:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myDjangoApp', '0003_auto_20161024_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderapplication',
            name='operatedate',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='operatedate',
            field=models.DateTimeField(),
        ),
    ]
