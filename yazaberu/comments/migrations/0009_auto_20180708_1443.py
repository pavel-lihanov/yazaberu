# Generated by Django 2.0.6 on 2018-07-08 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0008_auto_20180612_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='viewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='viewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notification',
            name='viewed',
            field=models.BooleanField(default=False),
        ),
    ]
