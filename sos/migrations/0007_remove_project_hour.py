# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 09:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sos', '0006_auto_20170227_1043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='hour',
        ),
    ]