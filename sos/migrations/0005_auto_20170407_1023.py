# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-07 08:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sos', '0004_material_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material_group',
            name='parrent_name',
        ),
        migrations.AddField(
            model_name='material_group',
            name='parrent',
            field=models.ManyToManyField(related_name='_material_group_parrent_+', to='sos.Material_Group'),
        ),
    ]
