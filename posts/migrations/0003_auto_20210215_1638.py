# Generated by Django 3.1.6 on 2021-02-15 16:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20210215_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(verbose_name=datetime.datetime(2021, 2, 15, 16, 38, 53, 593274)),
        ),
    ]
