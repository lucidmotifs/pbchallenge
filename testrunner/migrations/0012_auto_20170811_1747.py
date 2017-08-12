# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-11 17:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testrunner', '0011_auto_20170810_0234'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testruninstance',
            options={'ordering': ('-created_on', 'executed_on')},
        ),
        migrations.AlterField(
            model_name='testrun',
            name='modules',
            field=models.ManyToManyField(blank=True, to='testrunner.TestModule'),
        ),
    ]
