# Generated by Django 3.1.6 on 2021-02-16 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210216_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='followers',
            field=models.JSONField(blank=True, default=[], null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='following',
            field=models.JSONField(blank=True, default=[], null=True),
        ),
    ]