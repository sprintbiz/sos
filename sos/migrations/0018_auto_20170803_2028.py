# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-03 18:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sos', '0017_auto_20170803_2023'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='address_id',
            new_name='address',
        ),
    ]
