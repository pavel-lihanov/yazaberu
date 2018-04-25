# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-22 13:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0007_auto_20180412_0804'),
        ('comments', '0004_auto_20180422_1354'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comments.Message')),
                ('parcel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transport.Parcel')),
                ('trip', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transport.Trip')),
            ],
        ),
    ]