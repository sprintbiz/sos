from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, UpdateView
from django.shortcuts import render, get_object_or_404,redirect
from sos.forms import CreateUserForm, invoice_material_formset,invoice_service_formset, EventForm, ManufacturerForm, MaterialForm, MaterialGroupForm, MaterialTransactionForm, OrganizationForm, PasswordChangeCustomForm, ProjectForm, ServiceForm, InvoiceForm, TaxForm, UserForm
from sos.models import Event, Invoice, Invoice_Material, Invoice_Service, Manufacturer, Material, Material_Group, Material_Transactions, Organization, Project, Service, Tax, Warehouse
from django.contrib.auth.models import User
from django.forms import extras, inlineformset_factory
from django.forms import modelformset_factory
import cStringIO as StringIO
from django.template.loader import get_template
from django.template import Context
from cgi import escape
from django.db.models import F,ExpressionWrapper,FloatField, Sum, Value as V, TextField
from django.db.models.functions import Coalesce, Concat
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.messages.views import SuccessMessageMixin
import json
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
import datetime
from django.utils import timezone
from django.db import connection
from itertools import chain

class RedirectView(View):
    def get(self, request):
        return render(request, 'dashboard.html')


class Dashboard(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        username = request.user.username
        truncate_month = connection.ops.date_trunc_sql('month','transaction_time')
        params = {'username' : username}
        params["name"] = "Sprintbiz"
        params["transactions"] = Material_Transactions.objects.extra({'transaction_month': truncate_month}).values('transaction_month','material__name').annotate(total_units = Sum('units'))

        return render(request, 'dashboard.html', params)

class InvoiceListView(ListView):
    title = 'Invoice List';
    model = Invoice      # shorthand for setting queryset = models.Car.objects.all()
    template_name = 'invoice.html'  # optional (the default is app_name/modelNameInLowerCase_list.html; which will look into your templates folder for that path and file)
    context_object_name = 'invoices'    #default is object_list as well as model's_verbose_name_list and/or model's_verbose_name_plural_list, if defined in the model's inner Meta class

class InvoicePrintView(View):
    def get(self, request, id):
        invoice_object = Invoice.objects.get(id=id)
        invoicem_service = Invoice_Service.objects.filter(invoice_id=id).annotate(service_name=F('service__name')
		                                                       ,price_per_hour=ExpressionWrapper( Coalesce(F('service__price_per_hour'), F('service__fixed_price') ), output_field=FloatField() )
															   ,value=ExpressionWrapper(Coalesce(F('service__price_per_hour') * F('quantity'), F('service__fixed_price') * F('quantity')), output_field=FloatField())
															   ,tax_value=ExpressionWrapper( Coalesce((F('service__price_per_hour') * F('quantity'))*F('service__tax__value')/100, (F('service__fixed_price') * F('quantity'))*F('service__tax__value')/100), output_field=FloatField() )
                                                               ,tax_prct=F('service__tax__value')
															   ,gross_value=ExpressionWrapper(
                                                                   Coalesce (
                                                                       (F('service__price_per_hour') * F('quantity'))+(F('service__price_per_hour') * F('quantity'))*F('service__tax__value')/100,
                                                                       (F('service__fixed_price') * F('quantity'))+(F('service__fixed_price') * F('quantity'))*F('service__tax__value')/100
                                                                   ), output_field=FloatField()
                                                               )
															   )
        invoicem_material = Invoice_Material.objects.filter(invoice_id=id).annotate(service_name=F('material__name')
		                                                       ,price_per_hour=ExpressionWrapper( F('material__price'), output_field=FloatField() )
															   ,value=ExpressionWrapper(F('material__price') * F('quantity'), output_field=FloatField())
															   ,tax_value=ExpressionWrapper( (F('material__price') * F('quantity'))*F('material__tax__value')/100, output_field=FloatField() )
                                                               ,tax_prct=F('material__tax__value')
															   ,gross_value=ExpressionWrapper(
                                                                    (F('material__price') * F('quantity'))+(F('material__price') * F('quantity'))*F('material__tax__value')/100, output_field=FloatField()
															   ))
        invoice_detail_object = chain(invoicem_material, invoicem_service)
        invoice_service_total = Invoice_Service.objects.filter(invoice_id=id).aggregate(
            total_tax=Sum(
                Coalesce (
                    (F('service__price_per_hour') * F('quantity'))*F('service__tax__value')/100,
                    (F('service__fixed_price') * F('quantity'))*F('service__tax__value')/100
                ), output_field=FloatField()
            ),
            total_net=Sum(
                Coalesce (
                    F('service__price_per_hour') * F('quantity'),
                    F('service__fixed_price') * F('quantity')
                ), output_field=FloatField()
            ),
            total_gross=Sum(
                Coalesce (
                    (F('service__price_per_hour') * F('quantity'))*F('service__tax__value')/100+F('service__price_per_hour') * F('quantity'),
                    (F('service__fixed_price') * F('quantity'))*F('service__tax__value')/100+F('service__fixed_price') * F('quantity'),
                ), output_field=FloatField()
            )
        )
        invoice_material_total = Invoice_Material.objects.filter(invoice_id=id).aggregate(
            total_tax=Sum(
                    (F('material__price') * F('quantity'))*F('material__tax__value')/100, output_field=FloatField()
            ),
            total_net=Sum(
                    F('material__price') * F('quantity'), output_field=FloatField()
            ),
            total_gross=Sum(
                    (F('material__price') * F('quantity'))*F('material__tax__value')/100+F('material__price') * F('quantity'), output_field=FloatField()
            )
        )
        invoice_total_tax = invoice_service_total['total_tax'] + invoice_material_total['total_tax']
        invoice_total_net = invoice_service_total['total_net'] + invoice_material_total['total_net']
        invoice_total_gross = invoice_service_total['total_gross'] + invoice_material_total['total_gross']
        return render(request,'invoice_print.html'  ,{'invoice_object' : invoice_object
                                                    , 'invoice_detail_object' : invoice_detail_object
                                                    , 'invoice_total_tax' : invoice_total_tax
                                                    , 'invoice_total_net' : invoice_total_net
                                                    , 'invoice_total_gross' : invoice_total_gross
                                                    }
                    )

class InvoiceEditView(UpdateView):
    action_url =''
    form_class = InvoiceForm
    model = Invoice
    template_name = 'invoice_create.html'
    success_url = 'invoice/'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        invoice_form = self.get_form(form_class)
        invoice_service_form = invoice_service_formset(instance = self.object, prefix='service')
        invoice_material_form = invoice_material_formset(instance = self.object, prefix='material')
        return self.render_to_response(
            self.get_context_data(invoice_form=invoice_form,
                                  invoice_service=invoice_service_form,
                                  invoice_material=invoice_material_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        invoice_service_form = invoice_service_formset(self.request.POST, instance=self.object, prefix='service')
        invoice_material_form = invoice_material_formset(self.request.POST, instance=self.object, prefix='material')
        if (form.is_valid() and invoice_service_form.is_valid() and invoice_material_form.is_valid()):
            return self.form_valid(form, invoice_service_form, invoice_material_form)
        else:
            return self.form_invalid(form, invoice_service_form, invoice_material_form)

    def form_valid(self, invoice_form, invoice_service_form, invoice_material_form):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        self.object = invoice_form.save()
        invoice_service_form.instance = self.object
        invoice_service_form.save()
        invoice_material_form.instance = self.object
        invoice_material_form.save()
        return HttpResponseRedirect(reverse('invoice-list'))

    def form_invalid(self, invoice_form, invoice_service_form, invoice_material_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(invoice=invoice_form,
                                  invoice_service=invoice_service_form,
                                  invoice_material=invoice_material_form))

class CreateInvoiceView(CreateView):
    action_url = '/invoice/new/'
    form_class = InvoiceForm
    model = Invoice
    template_name = 'invoice_create.html'
    success_url = 'invoice/'
    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        invoice_form = self.get_form(form_class)
        invoice_service_form = invoice_service_formset(prefix='service')
        invoice_material_form = invoice_material_formset(prefix='material')
        return self.render_to_response(
            self.get_context_data(invoice_form=invoice_form,
                                  invoice_service=invoice_service_form,
                                  invoice_material=invoice_material_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        invoice_service_form = invoice_service_formset(self.request.POST, prefix='service')
        invoice_material_form = invoice_material_formset(self.request.POST, prefix='material')
        if (form.is_valid() and invoice_service_form.is_valid() and invoice_material_form.is_valid()):
            return self.form_valid(form, invoice_service_form, invoice_material_form)
        else:
            return self.form_invalid(form, invoice_service_form, invoice_material_form)

    def form_valid(self, invoice_form, invoice_service_form, invoice_material_form):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        id = invoice_form.save()
        self.object = id

        invoice_material_form.instance = self.object
        materials = invoice_material_form.save(commit=False)
        for material in materials:
            transaction = Material_Transactions(user = self.request.user ,warehouse = material.warehouse, material = material.material, units = material.item, invoice = id)
            transaction.save()
        invoice_material_form.save()
        invoice_service_form.instance = self.object
        invoice_service_form.save()
        return HttpResponseRedirect(reverse('invoice-list'))

    def form_invalid(self, invoice_form, invoice_detail_form, invoice_material_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(invoice=invoice_form,
                                  invoice_detail=invoice_detail_form,
                                  invoice_material = invoice_material_form))


class TimescheetView(View):
    def get(self, request):
        title ='Timescheet'
        action_url = '/calendar/'
        event_form = EventForm()
        event_modal_form = EventForm(prefix='modal-event')
        return render(request,'calendar.html',{'action_url' : action_url,'title' : title, 'event_form' : event_form, 'event_modal_form' : event_modal_form})

    def post(self, request):
        title ='Timescheet'
        action_url = '/calendar/'
        id = request.POST.get('event-id','')
        project_id = request.POST.get('event-project-id','')
        start_date = request.POST.get('event-start-date','')
        end_date = request.POST.get('event-end-date','')
        name = request.POST.get('event-name','')
        hour = request.POST.get('event-hour','')
        type_code ='TS'

        modal_id = request.POST.get('modal-event-id','')
        if 'update' in request.POST:
            project_id = request.POST.get('modal-project-id','')
            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                raise Http404

            try:
                obj = Event.objects.get(id=id)
            except Event.DoesNotExist:
                obj = Event(project=project, start_date=start_date, end_date=end_date, type_code=type_code, name=name, hour=hour)
                obj.save()
            event_form = EventForm()
            event_modal_form = EventForm(prefix='modal-event')
            return render(request,'calendar.html',{'action_url' : action_url,'title' : title, 'event_form' : event_form, 'event_modal_form' : event_modal_form})

        if 'delete' in request.POST:
            try:
                event = Event.objects.get(id=modal_id)
            except Event.DoesNotExist:
                raise Http404
            event.delete()
            event_form = EventForm()
            event_modal_form = EventForm(prefix='modal-event')
            return render(request,'calendar.html',{'action_url' : action_url,'title' : title, 'event_form' : event_form, 'event_modal_form' : event_modal_form})

        event_form = EventForm(request.POST)
        if event_form.is_valid():
            new_event = event_form.save(commit=False)
            new_event.save()
            messages.success(request, 'Added new event ' + request.POST.get('name',''))


        return HttpResponseRedirect('/calendar/')

class CalendarResponce(View):
    def get(self, request):
        start = request.GET.get('start','')
        end = request.GET.get('end','')
        event_data = Event.objects.filter(start_date__gte = start,end_date__lt = end).annotate(start=F('start_date'), end=F('end_date'), title=F('name') ).values('id', 'title', 'start', 'end','hour','project')
        event_json = json.dumps(list(event_data), cls=DjangoJSONEncoder)
        return HttpResponse(event_json, content_type="application/json")

class JsonProject(View):
    def get(self, request):
        if request.method == 'GET' and 'id' in request.GET:
            project_id = request.GET.get('id','')
            project_data = Project.objects.filter(id = project_id).annotate(text=F('name')).values('id', 'text')
            project_json = json.dumps(list(project_data), cls=DjangoJSONEncoder)
            project_single_json = project_json[1:-1]
            return HttpResponse(project_single_json, content_type="application/json")
        else:
            project_data = Project.objects.annotate(text=F('name')).values('id', 'text')
            project_json = json.dumps(list(project_data), cls=DjangoJSONEncoder)
            return HttpResponse(project_json, content_type="application/json")

class JsonDaysNotFilled(View):
    def get(self, request):
        start = request.GET.get('start','')
        end = request.GET.get('end','')
        event_data = Event.objects.values('start_date').annotate(total_hours = Sum('hour'))
        event_json = json.dumps(list(event_data), cls=DjangoJSONEncoder)
        return HttpResponse(event_json, content_type="application/json")

class EventList(View):
    def get(self, request):
        title ='Timescheet'
        action_url1 = '/event/add/'
        action_url2 = '/event/edit/'
        template = 'calendar.html'
        event_form = EventForm()
        event_modal_form = EventForm(prefix='modal-event')
        return render(request,template,{'action_url1' : action_url1,'action_url2' : action_url2,'title' : title, 'event_form' : event_form, 'event_modal_form' : event_modal_form})

class EventEdit(View):
    def post(self, request):
        title ='Timescheet'
        action_url = '/event/'
        template = 'calendar.html'
        modal_id = request.POST.get('modal-event-id','')
        if 'delete' in request.POST:
            try:
                event = Event.objects.get(id=modal_id)
            except Event.DoesNotExist:
                raise Http404
            event.delete()

            return HttpResponseRedirect(action_url)

        if 'update' in request.POST:
            event = Event.objects.get(id=modal_id)
            event_form = EventForm(request.POST, instance=event, prefix='modal-event')
            if event_form.is_valid():
                changed_event = event_form.save(commit=False)
                changed_event.save()
            action_url1 = '/event/add/'
            action_url2 = '/event/edit/'
            event_modal_form = EventForm(prefix='modal-event')
            return HttpResponseRedirect(action_url)




class EventCreate(View):
    def post(self, request):
        title ='Timescheet'
        action_url = '/event/'
        id = request.POST.get('event-id','')
        project_id = request.POST.get('event-project-id','')
        start_date = request.POST.get('event-start-date','')
        end_date = request.POST.get('event-end-date','')
        name = request.POST.get('event-name','')
        hour = request.POST.get('event-hour','')
        type_code ='TS'

        modal_id = request.POST.get('modal-event-id','')

        event_form = EventForm(request.POST)
        if event_form.is_valid():
            new_event = event_form.save(commit=False)
            new_event.save()
            messages.success(request, 'Added new event ' + request.POST.get('name',''))
        return HttpResponseRedirect(action_url)

class ManufacturerList(ListView):
    title = 'Manufacturer List'
    template_name = 'manufacturer_list.html'
    model = Manufacturer
    form_class = ManufacturerForm

class ManufacturerCreate(SuccessMessageMixin, CreateView):
    title = 'Manufacturer Create'
    template_name = 'manufacturer_create.html'
    model = Manufacturer
    form_class = ManufacturerForm
    success_message = "%(name)s was created successfully"
    def get_success_url(self):
        return reverse('manufacturer-list')

class MaterialList(ListView):
    title = 'Material List'
    template_name = 'material_list.html'
    model = Material
    form_class = MaterialForm

class MaterialCreate(SuccessMessageMixin, CreateView):
    title = 'Material Create'
    template_name = 'material_create.html'
    model = Material
    form_class = MaterialForm
    success_message = "%(name)s was created successfully"
    def get_success_url(self):
        return reverse('material-list')

class MaterialDelete(DeleteView):
    title = 'Material Delete'
    template_name = 'material_confirm_delete.html'
    model = Material
    success_url = reverse_lazy('material-list')
    success_message = "Material was deleted successfully"
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(MaterialDelete, self).delete(request, *args, **kwargs)

class MaterialDetail(DetailView):
    title = 'Material Detail'
    template_name = 'material_detail.html'
    model = Material
    def get_context_data(self, **kwargs):
        context = super(MaterialDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class MaterialEdit(UpdateView):
    title = 'Material Edit'
    template_name = 'material_edit.html'
    model = Material
    form_class = MaterialForm

class MaterialGroupList(ListView):
    title = 'Material Group List'
    template_name = 'material_group_list.html'
    model = Material_Group
    form_class = MaterialGroupForm

class MaterialGroupCreate(SuccessMessageMixin, CreateView):
    title = 'Material Group Create'
    template_name = 'material_group_create.html'
    model = Material_Group
    form_class = MaterialGroupForm
    success_message = "%(name)s was created successfully"
    def get_success_url(self):
        return reverse('material-group-list')

class MaterialGroupDelete(DeleteView):
    title = 'Material Group Delete'
    template_name = 'material_group_confirm_delete.html'
    model = Material_Group
    success_url = reverse_lazy('material-group-list')
    success_message = "Material Group was deleted successfully"
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(MaterialGroupDelete, self).delete(request, *args, **kwargs)

class MaterialGroupDetail(DetailView):
    title = 'Material Group Detail'
    template_name = 'material_group_detail.html'
    model = Material_Group
    def get_context_data(self, **kwargs):
        context = super(MaterialGroupDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class MaterialGroupEdit(UpdateView):
    title = 'Material Group Edit'
    template_name = 'material_group_edit.html'
    model = Material_Group
    form_class = MaterialGroupForm

class MaterialTransactionDelete(DeleteView):
    title = 'Material Transaction Delete'
    template_name = 'material_transaction_confirm_delete.html'
    model = Material_Transactions
    success_url = reverse_lazy('material-transaction-list')
    success_message = "Material Transaction was deleted successfully"
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(MaterialTransactionDelete, self).delete(request, *args, **kwargs)

class MaterialTransactionList(ListView):
    title = 'Material Transaction List'
    template_name = 'material_transaction_list.html'
    model = Material_Transactions
    form_class = MaterialTransactionForm

class MaterialTransactionEdit(UpdateView):
    title = 'Material Transaction Edit'
    template_name = 'material_transaction_edit.html'
    model = Material_Transactions
    form_class = MaterialTransactionForm

class TaxList(ListView):
    title = 'Tax List'
    template_name = 'tax_list.html'
    model = Tax
    form_class = TaxForm

class TaxCreate(SuccessMessageMixin, CreateView):
    title = 'Tax Create'
    template_name = 'tax_create.html'
    model = Tax
    form_class = TaxForm
    success_message = "%(name)s was created successfully"
    def get_success_url(self):
        return reverse('tax-list')

class TaxEdit(UpdateView):
    title = 'Tax Edit'
    template_name = 'tax_edit.html'
    model = Tax
    form_class = TaxForm

class TaxDelete(DeleteView):
    title = 'Tax Delete'
    template_name = 'tax_confirm_delete.html'
    model = Tax
    success_url = reverse_lazy('tax-list')
    success_message = "Tax was deleted successfully"
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(TaxDelete, self).delete(request, *args, **kwargs)

class TaxDetail(DetailView):
    title = 'Tax Detail'
    template_name = 'tax_detail.html'
    model = Tax
    def get_context_data(self, **kwargs):
        context = super(TaxDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class OrganizationList(ListView):
    title = 'Organization List'
    template_name = 'organization_list.html'
    model = Organization
    form_class = OrganizationForm

class OrganizationCreate(SuccessMessageMixin, CreateView):
    title = 'Organization Create'
    template_name = 'organization_create.html'
    model = Organization
    form_class = OrganizationForm
    success_message = "%(name)s was created successfully"
    def get_success_url(self):
        return reverse('organization-list')

class OrganizationEdit(UpdateView):
    title = 'Organization Edit'
    template_name = 'organization_edit.html'
    model = Organization
    form_class = OrganizationForm

class OrganizationDelete(DeleteView):
    title = 'Organization Delete'
    template_name = 'organization_confirm_delete.html'
    model = Organization
    success_url = reverse_lazy('organization-list')
    success_message = "Organization was deleted successfully"
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(OrganizationDelete, self).delete(request, *args, **kwargs)

class OrganizationDetail(DetailView):
    title = 'Organization Detail'
    template_name = 'organization_detail.html'
    model = Organization
    def get_context_data(self, **kwargs):
        context = super(OrganizationDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class ProjectList(ListView):
    title = 'Project List'
    template_name = 'project_list.html'
    model = Project
    form_class = ProjectForm

class ProjectCreate(SuccessMessageMixin, CreateView):
    title = 'Project Create'
    template_name = 'project_create.html'
    model = Project
    form_class = ProjectForm
    success_message = "%(name)s was created successfully"
    def get_success_url(self):
        return reverse('project-list')

class ProjectDelete(DeleteView):
    title = 'Project Delete'
    template_name = 'project_confirm_delete.html'
    model = Project
    success_url = reverse_lazy('project-list')
    success_message = "Project was deleted successfully"
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ProjectDelete, self).delete(request, *args, **kwargs)

class ProjectDetail(DetailView):
    title = 'Project Detail'
    template_name = 'project_detail.html'
    model = Project
    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        return context

class ProjectEdit(UpdateView):
    title = 'Project Edit'
    template_name = 'project_edit.html'
    model = Project
    form_class = ProjectForm

class ServiceList(ListView):
    title = 'Service List'
    template_name = 'service_list.html'
    model = Service
    form_class = ServiceForm

class ServiceCreate(SuccessMessageMixin, CreateView):
    title = 'Service Create'
    template_name = 'service_create.html'
    model = Service
    form_class = ServiceForm
    success_message = "%(name)s was created successfully"
    def get_success_url(self):
        return reverse('service-list')

class ServiceEdit(UpdateView):
    title = 'Service Edit'
    template_name = 'service_edit.html'
    model = Service
    form_class = ServiceForm

class ServiceDelete(DeleteView):
    title = 'Service Delete'
    template_name = 'service_confirm_delete.html'
    model = Service
    success_url = reverse_lazy('service-list')
    success_message = "Service was deleted successfully"
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ServiceDelete, self).delete(request, *args, **kwargs)

class ServiceDetail(DetailView):
    title = 'Service Detail'
    template_name = 'service_detail.html'
    model = Service
    def get_context_data(self, **kwargs):
        context = super(ServiceDetail, self).get_context_data(**kwargs)
        return context

class ProfileCreateView(View):
    def get(self, request):
        title ='Create User'
        template = 'profile_create.html'
        profile_create_form = CreateUserForm()
        return render(request,template,{'title' : title, 'profile_form' : profile_create_form})

    def post(self, request):
        title ='Create User'
        template = 'profile_create.html'
        profile_create_form = CreateUserForm(request.POST)
        if profile_create_form.is_valid():
            profile_create_form.save()
            messages.success(request, 'Profile for ' + request.POST.get("username", "") + ' created')
        return render(request,template,{'title' : title, 'profile_form' : profile_create_form})

class ProfileView(View):
    def get(self, request):
        title ='Profile'
        template = 'profile.html'
        user = User.objects.get(id=request.user.id)
        user_name = user.username
        profile_form = UserForm(instance=user)
        return render(request,template,{'title' : title, 'profile_form' : profile_form, 'user_name' : user_name})

    def post(self, request, *args, **kwargs):
        title ='Profile'
        template = 'profile.html'
        user = User.objects.get(id=request.user.id)
        user_name = user.username
        profile_form = UserForm(request.POST, instance=user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile was changed')
            return redirect('profile')
        else:
            return render(request,template,{'title' : title, 'profile_form' : profile_form, 'user_name' : user_name})

class ProfileChangePassword(View):
    def get(self, request, *args, **kwargs):
        title ='Change Password'
        template = 'profile_password_change.html'
        password_form = PasswordChangeCustomForm(request.user)
        return render(request, 'profile_password_change.html', {'password_form': password_form})

    def post(self, request, *args, **kwargs):
        title ='Change Password'
        template = 'profile_password_change.html'
        password_form = PasswordChangeCustomForm(request.user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, 'Password was changed')
            return redirect('profile')
        else:
            return render(request, 'profile_password_change.html', {'password_form': password_form})
