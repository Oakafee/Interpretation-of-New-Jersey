# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-23 15:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inj', '0006_auto_20170320_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='thematic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='theme', to='inj.Article'),
        ),
    ]
