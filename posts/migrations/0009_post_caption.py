# Generated by Django 3.1.6 on 2021-02-15 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20210215_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='caption',
            field=models.TextField(blank=True, null=True),
        ),
    ]