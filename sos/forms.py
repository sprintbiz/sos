from django import forms
from sos.models import Code, Event, Invoice, Invoice_Material, Invoice_Service, Material, Organization, Project, Service,  Tax
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from djangoformsetjs.utils import formset_media_js
from django.utils.translation import ugettext_lazy
from django.forms.models import inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm

class InvoiceForm(forms.ModelForm):
    name = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control',}))
    type =  forms.ModelChoiceField(queryset=Code.objects.all().filter(entity='INVOICE', schema='TYPE'), widget= forms.Select(attrs={'class': 'select2' }))
    create_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))
    payment_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))
    status = forms.ModelChoiceField(queryset=Code.objects.all().filter(entity='INVOICE', schema='STATUS'), widget= forms.Select(attrs={'class': 'select2' }))
    company = forms.ModelChoiceField(queryset = Organization.objects.all().filter(org_type__name='Company'), widget=forms.Select(attrs={'class':'select2'}))
    customer = forms.ModelChoiceField(queryset = Organization.objects.all().filter(org_type__name='Customer'), widget=forms.Select(attrs={'class':'select2'}))
    literal_value = forms.CharField(widget= forms.Textarea(attrs={'class': 'form-control',}))
    payment_method = forms.ModelChoiceField(queryset=Code.objects.all().filter(entity='INVOICE', schema='PAYMENT_METHOD'), widget= forms.Select(attrs={'class': 'select2' }))
    class Meta:
        model = Invoice
        fields = ['id','name', 'create_date', 'payment_date','status','company','customer', 'literal_value','payment_method']

class InvoiceServiceForm(forms.ModelForm):
    hour = forms.CharField(required =False, widget= forms.TextInput(attrs={'class': 'form-control',}))
    service = forms.ModelChoiceField(required =False, queryset = Service.objects.all(), widget=forms.Select(attrs={'class':'select2'}))

    class Meta():
        model = Service
        fields = ['service','hour',]

class InvoiceMaterialForm(forms.ModelForm):
    item = forms.CharField(required =False, widget= forms.TextInput(attrs={'class': 'form-control',}))
    material = forms.ModelChoiceField(required =False, queryset = Material.objects.all(), widget=forms.Select(attrs={'class':'select2'}))

    class Meta():
        model = Material
        fields = ['material','item',]

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

class MaterialForm(forms.ModelForm):
    name = forms.CharField(required =True, label='Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'material-name', }))
    tax = forms.ModelChoiceField(queryset = Tax.objects.all() , label='Tax', widget= forms.Select(attrs={'class': 'select','id':'material-tax', }))
    group = forms.ModelChoiceField(queryset = Code.objects.all().filter(entity='MATERIAL', schema='GROUP') , label='Group', widget= forms.Select(attrs={'class': 'select','id':'material-group', }))
    manufacturer = forms.ModelChoiceField(queryset = Organization.objects.filter(org_type__type = 'MANU') , label='Manufacturer', widget= forms.Select(attrs={'class': 'select','id':'material-manufacturer', }))
    dealer = forms.ModelChoiceField(queryset = Organization.objects.filter(org_type__type = 'DEAL') , label='Dealer', widget= forms.Select(attrs={'class': 'select','id':'material-dealer', }))
    price = forms.DecimalField(required =False, label='Price', widget= forms.NumberInput(attrs={'class': 'form-control','id':'material-price', }))
    class Meta:
        model = Material
        fields = ['name','price','tax','group','manufacturer','dealer']

class OrganizationForm(forms.ModelForm):
    name = forms.CharField(required =True, label='Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-name', }))
    street_name = forms.CharField(required =False, label='Street Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-street-name', }))
    street_number = forms.CharField(required =False, label='Street Number', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-street-number', }))
    zip_code = forms.CharField(required =False, label='Zip Code', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-zip-code', }))
    city = forms.CharField(required =False, label='City', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-city', }))
    country = forms.CharField(required =False, label='Country', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-country', }))
    phone = forms.CharField(required =False, label='Phone', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-phone', }))
    email = forms.CharField(required =False, label='Email', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-email', }))
    org_nbr_1 = forms.CharField(required =False, label='NIP', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-org-nbr-1', }))
    org_nbr_2 = forms.CharField(required =False, label='REGON', widget= forms.TextInput(attrs={'class': 'form-control','id':'organization-org-nbr-2', }))
    org_type = forms.ModelChoiceField(required =False, label='Code', widget= forms.Select(attrs={'class': 'select','id':'organization-code', }), queryset=Code.objects.all().filter(entity='ORGANIZATION') )
    class Meta:
        model = Organization
        fields = ['name','street_name','street_number','zip_code','city','country','phone','email','org_nbr_1','org_nbr_2','org_type']

class ProjectForm(forms.ModelForm):
    name = forms.CharField(required =True, label='Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'project-name', }))
    customer = forms.ModelChoiceField(queryset = Organization.objects.all().filter(org_type = 1) , label='Customer', widget= forms.Select(attrs={'class': 'form-control','id':'project-customer', }))
    code = forms.CharField(required =True, label='Code', widget= forms.TextInput(attrs={'class': 'form-control','id':'project-code', }))
    class Meta:
        model = Project
        fields = ['name','code','customer']


class ServiceForm(forms.ModelForm):
    name = forms.CharField(required =True, label='Name', widget= forms.TextInput(attrs={'class': 'form-control','id':'service-name', }))
    tax = forms.ModelChoiceField(queryset = Tax.objects.all() , label='Tax', widget= forms.Select(attrs={'class': 'form-control','id':'service-tax', }))
    price_per_hour = forms.DecimalField(required =False, label='Price Per Hour', widget= forms.TextInput(attrs={'class': 'form-control','id':'service-price-per-hour', }))
    fixed_price = forms.DecimalField(required =False, label='Fixed Price', widget= forms.TextInput(attrs={'class': 'form-control','id':'service-fixed-price', }))
    class Meta:
        model = Service
        fields = ['name','tax','price_per_hour','fixed_price']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Email', 'aria-describedby' : 'basic-addon1'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password', 'aria-describedby' : 'basic-addon2'}))

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class PasswordChangeCustomForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeCustomForm, self).__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

invoice_service_formset = inlineformset_factory(Invoice, Invoice_Service, form=InvoiceServiceForm, extra=1, can_delete=True)
invoice_material_formset = inlineformset_factory(Invoice, Invoice_Material, form=InvoiceMaterialForm, extra=1, can_delete=True)
