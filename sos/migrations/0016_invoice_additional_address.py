# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-03 17:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sos', '0015_auto_20170730_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='additional_address',
            field=models.CharField(default=0, max_length=1),
            preserve_default=False,
        ),
    ]
