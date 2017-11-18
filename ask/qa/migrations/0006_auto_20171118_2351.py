# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-18 18:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0005_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='finish',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='start',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
