# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-20 22:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('draw', '0010_auto_20160630_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debate',
            name='venue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='venues.Venue'),
        ),
    ]
