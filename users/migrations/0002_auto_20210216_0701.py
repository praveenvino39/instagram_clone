# Generated by Django 3.1.6 on 2021-02-16 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='followers',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='following',
            field=models.JSONField(blank=True, null=True),
        ),
    ]