# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-22 18:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sos', '0012_auto_20170622_2012'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice_service',
            old_name='hour',
            new_name='quantity',
        ),
    ]