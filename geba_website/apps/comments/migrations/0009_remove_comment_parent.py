# Generated by Django 2.0.4 on 2018-04-26 01:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0008_auto_20180128_0142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
    ]
