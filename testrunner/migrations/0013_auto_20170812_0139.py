# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-12 01:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testrunner', '0012_auto_20170811_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testrun',
            name='modules',
            field=models.ManyToManyField(to='testrunner.TestModule'),
        ),
    ]