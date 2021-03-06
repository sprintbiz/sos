# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-03 18:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sos', '0016_invoice_additional_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='additional_address',
            new_name='additional_address_ind',
        ),
        migrations.AddField(
            model_name='organization',
            name='address_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sos.Address'),
            preserve_default=False,
        ),
    ]
