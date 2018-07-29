# Generated by Django 2.0.6 on 2018-07-29 05:42

import apps.blog.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('vote_score', models.FloatField(db_index=True, default=0)),
                ('num_vote_up', models.PositiveIntegerField(db_index=True, default=0)),
                ('num_vote_down', models.PositiveIntegerField(db_index=True, default=0)),
                ('slug', models.SlugField(unique=True)),
                ('publish_date', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=apps.blog.models.upload_location, width_field='width_field')),
                ('width_field', models.IntegerField(default=0)),
                ('height_field', models.IntegerField(default=0)),
                ('image_caption', models.CharField(blank=True, max_length=200, null=True)),
                ('draft', models.BooleanField(default=False)),
                ('body', models.TextField()),
                ('keywords', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-vote_score', '-num_vote_up', '-publish_date', '-modified'],
            },
        ),
    ]
