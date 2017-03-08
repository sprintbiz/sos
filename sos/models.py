# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.core.urlresolvers import reverse


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

    def get_absolute_url(self):
        return reverse('status-edit', kwargs={'pk': self.id})

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

class Organization (models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    street_name = models.CharField(max_length=60, blank=True)
    street_number = models.CharField(max_length=10, blank=True)
    zip_code = models.CharField(max_length=60, blank=True)
    city = models.CharField(max_length=60, blank=True)
    country = models.CharField(max_length=60, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.CharField(max_length=60, blank=True)
    org_nbr_1 = models.CharField(max_length=30, blank=True)
    org_nbr_2 = models.CharField(max_length=30, blank=True)
    org_type = models.ForeignKey(Code)
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

class Service (models.Model):
    id = models.AutoField(primary_key=True)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    price_per_hour  = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fixed_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Service'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service-edit', kwargs={'pk': self.id})

class Invoice (models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    create_date = models.DateField()
    payment_date = models.DateField()
    status = models.ForeignKey(Code, related_name='code_status')
    company = models.ForeignKey(Organization, related_name='organization_company')
    customer = models.ForeignKey(Organization, related_name='organization_customer')
    payment_method = models.ForeignKey(Code, related_name='code_payment_method')
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
