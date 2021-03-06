# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-08 19:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TestRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_run', models.DateTimeField()),
                ('last_result', models.CharField(choices=[('pass', 'pass'), ('fail', 'fail'), ('error', 'error')], default='Null', max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('created_on', models.DateTimeField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TestRunInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interface', models.CharField(choices=[('ssh', 'ssh'), ('lfs', 'local')], default='ssh', max_length=20)),
                ('created_on', models.DateTimeField()),
                ('executed_on', models.DateTimeField()),
                ('environment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testrunner.Environment')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created_on',),
            },
        ),
    ]
