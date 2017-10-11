# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-09 17:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Audit', '0002_auto_20171009_1757'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command', models.TextField(max_length=1024)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('session_log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Audit.SessionLog')),
            ],
        ),
    ]
