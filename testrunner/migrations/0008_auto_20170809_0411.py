# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-09 04:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testrunner', '0007_auto_20170809_0353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testrun',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='testruns', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
