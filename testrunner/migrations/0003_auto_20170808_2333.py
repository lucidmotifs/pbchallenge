# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-08 23:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testrunner', '0002_auto_20170808_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testrun',
            name='last_run',
            field=models.DateTimeField(null=True),
        ),
    ]
