# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-08 02:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leadership', '0003_leader_display_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leader',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Member'),
        ),
    ]