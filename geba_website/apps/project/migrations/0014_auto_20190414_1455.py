# Generated by Django 2.1.7 on 2019-04-14 18:55

import apps.project.models
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_auto_20190331_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='header_height_field',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='header_image',
            field=models.ImageField(blank=True, height_field='header_height_field', null=True, upload_to=apps.project.models.upload_location, width_field='header_width_field'),
        ),
        migrations.AddField(
            model_name='project',
            name='header_width_field',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='title_in_header',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='projectpost',
            name='header_height_field',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='projectpost',
            name='header_image',
            field=models.ImageField(blank=True, height_field='header_height_field', null=True, upload_to=apps.project.models.upload_location, width_field='header_width_field'),
        ),
        migrations.AddField(
            model_name='projectpost',
            name='header_width_field',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='projectpost',
            name='title_in_header',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='publish_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 4, 14, 18, 55, 49, 281336, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='projectpost',
            name='publish_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 4, 14, 18, 55, 49, 280339, tzinfo=utc), null=True),
        ),
    ]
