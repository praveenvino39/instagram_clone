# Generated by Django 3.1.6 on 2021-02-16 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20210216_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
