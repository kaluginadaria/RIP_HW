# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-21 12:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hwApp', '0002_auto_20171221_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=128),
        ),
    ]
