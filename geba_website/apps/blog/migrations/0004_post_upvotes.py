# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-08-24 04:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_post_subtitle'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='upvotes',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
