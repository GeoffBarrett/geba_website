# Generated by Django 2.1.2 on 2018-10-10 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='height_field',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='width_field',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='projectpost',
            name='height_field',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='projectpost',
            name='width_field',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
