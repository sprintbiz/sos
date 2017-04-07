# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-05 17:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('type', models.CharField(max_length=30)),
                ('parrent', models.IntegerField(blank=True, null=True)),
                ('entity', models.CharField(max_length=30)),
                ('schema', models.CharField(max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Code',
                'verbose_name_plural': 'Codes',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('type_code', models.CharField(max_length=2)),
                ('name', models.CharField(max_length=300)),
                ('hour', models.DecimalField(decimal_places=2, max_digits=5)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Events',
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
                ('create_date', models.DateField()),
                ('payment_date', models.DateField()),
                ('literal_value', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
            },
        ),
        migrations.CreateModel(
            name='Invoice_Material',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('item', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sos.Invoice')),
            ],
            options={
                'verbose_name': 'Invoice Material',
                'verbose_name_plural': 'Invoice Materials',
            },
        ),
        migrations.CreateModel(
            name='Invoice_Service',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('hour', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sos.Invoice')),
            ],
            options={
                'verbose_name': 'Invoice Service',
                'verbose_name_plural': 'Invoice Services',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Material',
                'verbose_name_plural': 'Materials',
            },
        ),
        migrations.CreateModel(
            name='Material_Transactions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('transaction_time', models.DateTimeField(auto_now_add=True)),
                ('units', models.DecimalField(decimal_places=2, max_digits=5)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sos.Invoice')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sos.Material')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Material Transaction',
                'verbose_name_plural': 'Material Transactions',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('street_name', models.CharField(blank=True, max_length=60)),
                ('street_number', models.CharField(blank=True, max_length=10)),
                ('zip_code', models.CharField(blank=True, max_length=60)),
                ('city', models.CharField(blank=True, max_length=60)),
                ('country', models.CharField(blank=True, max_length=60)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('email', models.CharField(blank=True, max_length=60)),
                ('org_nbr_1', models.CharField(blank=True, max_length=30)),
                ('org_nbr_2', models.CharField(blank=True, max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('org_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sos.Code')),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organization',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('code', models.CharField(max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sos.Organization')),
            ],
            options={
                'verbose_name': 'Projects',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('price_per_hour', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('fixed_price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Service',
            },
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('value', models.DecimalField(decimal_places=2, max_digits=5)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Tax',
                'verbose_name_plural': 'Taxes',
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Warehouse',
                'verbose_name_plural': 'Warehouses',
            },
        ),
        migrations.AddField(
            model_name='service',
            name='tax',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sos.Tax'),
        ),
        migrations.AddField(
            model_name='material_transactions',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sos.Warehouse'),
        ),
        migrations.AddField(
            model_name='material',
            name='dealer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_dealer', to='sos.Organization'),
        ),
        migrations.AddField(
            model_name='material',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sos.Code'),
        ),
        migrations.AddField(
            model_name='material',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_manufacturer', to='sos.Organization'),
        ),
        migrations.AddField(
            model_name='material',
            name='tax',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sos.Tax'),
        ),
        migrations.AddField(
            model_name='invoice_service',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sos.Service'),
        ),
        migrations.AddField(
            model_name='invoice_material',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sos.Material'),
        ),
        migrations.AddField(
            model_name='invoice_material',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sos.Warehouse'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_company', to='sos.Organization'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_customer', to='sos.Organization'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='payment_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_payment_method', to='sos.Code'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_status', to='sos.Code'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_type', to='sos.Code'),
        ),
        migrations.AddField(
            model_name='event',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sos.Project'),
        ),
    ]
