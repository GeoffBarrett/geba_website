# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-08-17 02:45
from __future__ import unicode_literals

import apps.project.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20170816_2225'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='height_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='image',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to=apps.project.models.upload_location, width_field='width_field'),
        ),
        migrations.AddField(
            model_name='project',
            name='image_caption',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='keywords',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='width_field',
            field=models.IntegerField(default=0),
        ),
    ]
