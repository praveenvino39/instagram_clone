# Generated by Django 3.1.6 on 2021-02-15 16:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20210215_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comments',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(verbose_name=datetime.datetime(2021, 2, 15, 16, 40, 54, 241098)),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.JSONField(blank=True, null=True),
        ),
    ]