# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-30 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sos', '0013_auto_20170622_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('address_type', models.CharField(blank=True, max_length=10)),
                ('name', models.CharField(max_length=200)),
                ('street_name', models.CharField(blank=True, max_length=200)),
                ('street_number', models.CharField(blank=True, max_length=10)),
                ('zip_code', models.CharField(blank=True, max_length=60)),
                ('city', models.CharField(blank=True, max_length=200)),
                ('country', models.CharField(blank=True, max_length=200)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('email', models.CharField(blank=True, max_length=200)),
                ('bank_account', models.CharField(blank=True, max_length=40)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
    ]