# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-11 11:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sos', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'verbose_name': 'Invoice', 'verbose_name_plural': 'Invoices'},
        ),
        migrations.RenameField(
            model_name='invoice_service',
            old_name='unit',
            new_name='hour',
        ),
    ]
