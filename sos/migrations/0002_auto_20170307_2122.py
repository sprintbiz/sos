# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 20:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='payment_method',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, related_name='code_payment_method', to='sos.Code'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='code_status', to='sos.Code'),
        ),
    ]
