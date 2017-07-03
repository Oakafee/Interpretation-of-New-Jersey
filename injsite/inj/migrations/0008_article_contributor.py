# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-08 17:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inj', '0007_article_thematic'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='contributor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
