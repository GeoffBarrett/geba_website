# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-01-28 06:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0007_auto_20171021_1323'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-vote_score', '-num_vote_up', '-timestamp']},
        ),
    ]
