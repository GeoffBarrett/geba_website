# Generated by Django 2.1.2 on 2019-02-05 01:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20190131_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='publish_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 2, 5, 1, 39, 26, 22007, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='projectpost',
            name='publish_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 2, 5, 1, 39, 26, 21114, tzinfo=utc), null=True),
        ),
    ]
