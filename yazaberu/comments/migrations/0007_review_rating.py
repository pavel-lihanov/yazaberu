# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-29 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0006_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]
