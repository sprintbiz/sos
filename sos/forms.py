from django import forms
from sos.models import Invoice,Invoice_Details, Status, Company, Client, Customer, Service, Event, Project, Tax
from djangoformsetjs.utils import formset_media_js
from django.utils.translation import ugettext_lazy

class InvoiceForm(forms.ModelForm):
    name = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control',}))
    create_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))
    payment_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))
    status = forms.ModelChoiceField(queryset = Status.objects.all(), widget=forms.Select(attrs={'class':'select2'}))
    company = forms.ModelChoiceField(queryset = Company.objects.all(), widget=forms.Select(attrs={'class':'select2'}))
    client = forms.ModelChoiceField(queryset = Client.objects.all(), widget=forms.Select(attrs={'class':'select2'}))
    literal_value = forms.CharField(widget= forms.Textarea(attrs={'class': 'form-control',}))
    class Meta:
        model = Invoice
        fields = ['id','name', 'create_date', 'payment_date','status','company','client', 'literal_value',]

class InvoiceDetailForm(forms.ModelForm):
    hour = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control',}))
    service = forms.ModelChoiceField(queryset = Service.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))

    class Media(object):
        js = formset_media_js

    class Meta():
        model = Invoice_Details
        fields = ['service','hour',]

class EventForm(forms.ModelForm):
    project = forms.ModelChoiceField(required =False, label='Project', queryset = Project.objects.all(), widget=forms.Select(attrs={'style':'width: 100%','class':'project-select', 'id':'project-select'}))
    name = forms.CharField(required =False, label='Description', widget= forms.Textarea(attrs={'class': 'form-control','id':'event-name', }))
    hour = forms.CharField(required =False, label='Hour', widget= forms.TextInput(attrs={'class': 'form-control','id':'event-hour',}))
    start_date = forms.DateField(required =False, label='Start Date', widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'id':'event-start-date', }))
    end_date = forms.DateField(required =False, label='End Date', widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'id':'event-end-date',}))
    type_code = forms.CharField(required =False, label='Event Type', initial='TS', widget= forms.TextInput(attrs={'readonly' : 'True','class': 'form-control','id':'event-type'}))
    class Meta:
        model = Event
        fields = ['id','name', 'hour','start_date','end_date','type_code','project']

class EventForm(forms.ModelForm):
    project = forms.ModelChoiceField(required =False, label='Project', queryset = Project.objects.all(), widget=forms.Select(attrs={'style':'width: 100%','class':'project-select', 'id':'project-select'}))
    name = forms.CharField(required =False, label='Description', widget= forms.Textarea(attrs={'class': 'form-control','id':'event-name', }))
    hour = forms.CharField(required =False, label='Hour', widget= forms.TextInput(attrs={'class': 'form-control','id':'event-hour',}))
    start_date = forms.DateField(required =False, label='Start Date', widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'id':'event-start-date', }))
    end_date = forms.DateField(required =False, label='End Date', widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'id':'event-end-date',}))
    type_code = forms.CharField(required =False, label='Event Type', initial='TS', widget= forms.TextInput(attrs={'readonly' : 'True','class': 'form-control','id':'event-type'}))
    class Meta:
        model = Event
        fields = ['id','name', 'hour','start_date','end_date','type_code','project']

class TaxForm(forms.ModelForm):
    name = forms.CharField(required =True, label='Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'tax-name', }))
    value = forms.CharField(required =True, label='Value', widget= forms.TextInput(attrs={'class': 'form-control','id':'tax-value', }))
    class Meta:
        model = Tax
        fields = ['name','value']

class CustomerForm(forms.ModelForm):
    name = forms.CharField(required =True, label='Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'customer-name', }))
    street_name = forms.CharField(required =True, label='Street Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'customer-street-name', }))
    street_number = forms.CharField(required =True, label='Street Number', widget= forms.TextInput(attrs={'class': 'form-control','id':'customer-street-number', }))
    zip_code = forms.CharField(required =True, label='Zip Code', widget= forms.TextInput(attrs={'class': 'form-control','id':'customer-zip-code', }))
    city = forms.CharField(required =True, label='City', widget= forms.TextInput(attrs={'class': 'form-control','id':'customer-city', }))
    country = forms.CharField(required =True, label='Country', widget= forms.TextInput(attrs={'class': 'form-control','id':'customer-country', }))
    phone = forms.CharField(required =True, label='Phone', widget= forms.TextInput(attrs={'class': 'form-control','id':'customer-phone', }))
    email = forms.CharField(required =True, label='Email', widget= forms.TextInput(attrs={'class': 'form-control','id':'customer-email', }))
    code = forms.CharField(required =True, label='Code', widget= forms.TextInput(attrs={'class': 'form-control','id':'customer-code', }))
    class Meta:
        model = Customer
        fields = ['name','street_name','street_number','zip_code','city','country','phone','email','code']
