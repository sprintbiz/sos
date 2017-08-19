# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from datetime import datetime

class Code(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    parrent = models.IntegerField(blank=True, null=True)
    entity = models.CharField(max_length=30)
    schema = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Code'
        verbose_name_plural = 'Codes'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('code-edit', kwargs={'pk': self.id})

class Tax (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=False)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tax'
        verbose_name_plural = 'Taxes'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tax-edit', kwargs={'pk': self.id})


class Address (models.Model):

    id = models.AutoField(primary_key=True)
    address_type = models.CharField(max_length=10, blank=True)
    name = models.CharField(max_length=200)
    street_name = models.CharField(max_length=200, blank=True)
    street_number = models.CharField(max_length=10, blank=True)
    zip_code = models.CharField(max_length=60, blank=True)
    city = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.CharField(max_length=200, blank=True)
    bank_account = models.CharField(max_length=40, blank=True)
    add_code1 = models.CharField(max_length=100, blank=True)
    add_code2 = models.CharField(max_length=100, blank=True)
    add_code3 = models.CharField(max_length=100, blank=True)
    add_code4 = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('address-edit', kwargs={'pk': self.id})

class Organization (models.Model):

    id = models.AutoField(primary_key=True)
    address = models.ForeignKey(Address)
    name = models.CharField(max_length=200)
    street_name = models.CharField(max_length=200, blank=True)
    street_number = models.CharField(max_length=10, blank=True)
    zip_code = models.CharField(max_length=60, blank=True)
    city = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.CharField(max_length=200, blank=True)
    org_nbr_1 = models.CharField(max_length=30, blank=True)
    org_nbr_2 = models.CharField(max_length=30, blank=True)
    org_type = models.ForeignKey(Code)
    bank_account = models.CharField(max_length=40, blank=True)
    is_owner = models.NullBooleanField()
    is_customer = models.NullBooleanField()
    is_dealer = models.NullBooleanField()
    is_manufacturer = models.NullBooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organization'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organization-edit', kwargs={'pk': self.id})


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Organization)
    name = models.CharField(max_length=300)
    code = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Projects'
        verbose_name_plural = 'Projects'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project-edit', kwargs={'pk': self.id})

class Unit(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'

    def __unicode__(self):
        return self.name

class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'

    def __unicode__(self):
        return self.name

class Invoice (models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(Code, related_name='invoice_type')
    name = models.CharField(max_length=10)
    create_date = models.DateField()
    sales_date = models.DateField(blank=True, null=True)
    payment_date = models.DateField()
    status = models.ForeignKey(Code, related_name='invoice_status')
    additional_address_ind = models.CharField(max_length=1)
    company = models.ForeignKey(Organization, related_name='organization_company')
    customer = models.ForeignKey(Organization, related_name='organization_customer')
    payment_method = models.ForeignKey(Code, related_name='invoice_payment_method')
    literal_value = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('invoice', args=[str(self.id),str(self.name)])

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.sales_date:
            self.sales_date = self.create_date
        super(Invoice, self).save(*args, **kwargs)

class Material_Group (models.Model):
    id = models.AutoField(primary_key=True)
    parrent = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Material Group'
        verbose_name_plural = 'Material Groups'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('material-group-edit', kwargs={'pk': self.id})

class Manufacturer (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Manufacturer'
        verbose_name_plural = 'Manufacturers'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('manufacturer-edit', kwargs={'pk': self.id})

class Material (models.Model):
    id = models.AutoField(primary_key=True)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    unit = models.ForeignKey(Unit)
    group = models.ForeignKey(Material_Group)
    manufacturer = models.ForeignKey(Manufacturer)
    dealer = models.ForeignKey(Organization, related_name='organization_dealer', blank=True, null=True)
    price  = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materials'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('material-edit', kwargs={'pk': self.id})

class Service (models.Model):
    id = models.AutoField(primary_key=True)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price_per_hour  = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    fixed_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Service'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service-edit', kwargs={'pk': self.id})

class Invoice_Service (models.Model):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice)
    service = models.ForeignKey(Service)
    quantity  = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Invoice Service'
        verbose_name_plural = 'Invoice Services'

class Invoice_Material (models.Model):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice)
    material = models.ForeignKey(Material)
    warehouse = models.ForeignKey(Warehouse, blank=True, null=True)
    quantity  = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Invoice Material'
        verbose_name_plural = 'Invoice Materials'

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    type_code = models.CharField(max_length=2)
    name = models.CharField(max_length=300)
    hour  = models.DecimalField(max_digits=5, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Events'
        verbose_name_plural = 'Events'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event_list', kwargs={'id': self.id})

class Material_Transactions(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    transaction_time = models.DateTimeField(default=datetime.now)
    warehouse = models.ForeignKey(Warehouse)
    invoice = models.ForeignKey(Invoice)
    material = models.ForeignKey(Material)
    units = models.DecimalField(max_digits=5, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Material Transaction'
        verbose_name_plural = 'Material Transactions'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('material-transaction-edit', kwargs={'pk': self.id})
