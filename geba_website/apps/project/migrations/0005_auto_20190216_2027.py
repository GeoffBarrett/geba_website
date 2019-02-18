# Generated by Django 2.0.6 on 2019-02-17 01:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20190216_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='publish_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 2, 17, 1, 27, 4, 303673, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='projectpost',
            name='publish_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 2, 17, 1, 27, 4, 302676, tzinfo=utc), null=True),
        ),
    ]
