# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.core.urlresolvers import reverse

class Status(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'

    def __unicode__(self):
        return self.name

class Tax (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=False)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tax'
        verbose_name_plural = 'Tax'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tax-edit', kwargs={'pk': self.id})

class Company (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    street_name = models.CharField(max_length=60, blank=True)
    street_number = models.CharField(max_length=10, blank=True)
    zip_code = city = models.CharField(max_length=60, blank=True)
    city = models.CharField(max_length=60, blank=True)
    country = models.CharField(max_length=60, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.CharField(max_length=60, blank=True)
    code = models.CharField(max_length=30, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Company'

    def __unicode__(self):
        return self.name

class Client (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    street_name = models.CharField(max_length=60, blank=True)
    street_number = models.CharField(max_length=10, blank=True)
    zip_code = models.CharField(max_length=60, blank=True)
    city = models.CharField(max_length=60, blank=True)
    country = models.CharField(max_length=60, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.CharField(max_length=60, blank=True)
    code = models.CharField(max_length=30, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Client'

    def __unicode__(self):
        return self.name

class Customer (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    street_name = models.CharField(max_length=60, blank=True)
    street_number = models.CharField(max_length=10, blank=True)
    zip_code = models.CharField(max_length=60, blank=True)
    city = models.CharField(max_length=60, blank=True)
    country = models.CharField(max_length=60, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.CharField(max_length=60, blank=True)
    code = models.CharField(max_length=30, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customer'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('customer-edit', kwargs={'pk': self.id})

class Service (models.Model):
    id = models.AutoField(primary_key=True)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    price_per_hour  = models.DecimalField(max_digits=5, decimal_places=2)
    fixed_price = models.DecimalField(max_digits=5, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Service'

    def __unicode__(self):
        return self.name

class Invoice (models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    create_date = models.DateField()
    payment_date = models.DateField()
    status = models.ForeignKey(Status)
    company = models.ForeignKey(Company)
    client = models.ForeignKey(Client)
    literal_value = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('invoice', args=[str(self.id),str(self.name)])
    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoice'

    def __unicode__(self):
        return unicode(self.id) or u''

    def __int__(self):
        return self.id

class Invoice_Details (models.Model):
    id = models.AutoField(primary_key=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    hour  = models.DecimalField(max_digits=5, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Invoice detail'
        verbose_name_plural = 'Invoice detail'
    def __unicode__(self):
        return self.name

class Invoices (models.Model):
    name = models.ManyToManyField(Invoice)
    def __unicode__(self):
        return self.name

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client)
    name = models.CharField(max_length=300)
    code = models.CharField(max_length=30)
    hour  = models.DecimalField(max_digits=5, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Projects'
        verbose_name_plural = 'Projects'

    def __unicode__(self):
        return self.name

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
