# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-05 18:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material_transactions',
            name='invoice',
        ),
    ]
