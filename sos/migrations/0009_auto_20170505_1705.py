# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-05 15:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sos', '0008_auto_20170504_1426'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='is_client',
            new_name='is_customer',
        ),
    ]