# Generated by Django 2.1.7 on 2019-03-31 17:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_auto_20190331_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='publish_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 3, 31, 17, 10, 4, 914401, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='projectpost',
            name='publish_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 3, 31, 17, 10, 4, 913406, tzinfo=utc), null=True),
        ),
    ]
