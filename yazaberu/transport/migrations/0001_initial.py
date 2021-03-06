# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-06 07:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('globals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('duration', models.IntegerField()),
                ('delivered', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('lng', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('address', models.CharField(max_length=255)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transport.City')),
            ],
        ),
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='globals.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ends', to='transport.Location')),
                ('start', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='starts', to='transport.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transport', models.IntegerField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('duration', models.IntegerField()),
                ('rider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='globals.Profile')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transport.Route')),
            ],
        ),
        migrations.AddField(
            model_name='delivery',
            name='parcel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transport.Parcel'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='trip',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transport.Trip'),
        ),
    ]
