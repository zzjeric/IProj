# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-05 06:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myDjangoApp', '0005_auto_20161026_2226'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AlterField(
            model_name='orderapplication',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
