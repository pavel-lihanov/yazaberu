# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-12 05:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('globals', '0004_auto_20180408_0849'),
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=500)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='globals.Profile')),
            ],
        ),
    ]