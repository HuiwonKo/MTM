# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-10 10:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mentoring', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post_by_mentor',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
