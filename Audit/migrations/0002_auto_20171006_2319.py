# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Audit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='host_groups',
            field=models.ManyToManyField(blank=True, to='Audit.HostGroup'),
        ),
        migrations.AlterField(
            model_name='account',
            name='host_user_binds',
            field=models.ManyToManyField(blank=True, to='Audit.HostUserBind'),
        ),
    ]
