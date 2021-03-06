# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-09 03:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testrunner', '0006_auto_20170809_0122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testruninstance',
            options={'ordering': ('created_on', 'executed_on')},
        ),
        migrations.RenameField(
            model_name='testruninstance',
            old_name='requester',
            new_name='requested_by',
        ),
        migrations.AlterField(
            model_name='testrun',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='testruns', to=settings.AUTH_USER_MODEL),
        ),
    ]
