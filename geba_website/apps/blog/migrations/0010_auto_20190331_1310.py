# Generated by Django 2.1.7 on 2019-03-31 17:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20190331_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 3, 31, 17, 10, 4, 903436, tzinfo=utc), null=True),
        ),
    ]
