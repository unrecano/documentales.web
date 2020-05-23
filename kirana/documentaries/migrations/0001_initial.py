# Generated by Django 3.0.6 on 2020-05-23 03:52

import django.contrib.postgres.fields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Documentary',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('description', models.TextField()),
                ('year', models.CharField(max_length=4, null=True)),
                ('duration', models.PositiveIntegerField(null=True)),
                ('url', models.URLField()),
                ('sites', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), size=None)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('tags', models.ManyToManyField(related_name='documentaries', to='documentaries.Tag')),
            ],
            options={
                'verbose_name_plural': 'Documentaries',
            },
        ),
    ]