# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-08 15:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0003_delivery_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcel',
            name='comment',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='parcel',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='parcel',
            name='destination',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parcels_to', to='transport.Location'),
        ),
        migrations.AddField(
            model_name='parcel',
            name='due_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='parcel',
            name='max_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='parcel',
            name='origin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parcels_from', to='transport.Location'),
        ),
        migrations.AddField(
            model_name='parcel',
            name='value',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='parcel',
            name='weight',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='trip',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]