# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-10 00:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testrunner', '0009_auto_20170810_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testruninstance',
            name='executed_on',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='testruninstance',
            name='output',
            field=models.CharField(max_length=255, null=True),
        ),
    ]