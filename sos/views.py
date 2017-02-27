from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, UpdateView
from django.shortcuts import render, get_object_or_404,redirect
from sos.forms import EventForm, InvoiceDetailForm, OrganizationForm, ProjectForm, ServiceForm, InvoiceForm, TaxForm
from sos.models import Event, Invoice, Invoice_Details, Organization, Project, Service, Tax
from django.forms import extras, inlineformset_factory
from django.forms import modelformset_factory
import cStringIO as StringIO
from django.template.loader import get_template
from django.template import Context
from cgi import escape
from django.db.models import F,ExpressionWrapper,FloatField, Sum, Value as V, TextField
from django.db.models.functions import Coalesce, Concat
from django.contrib.auth import authenticate
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


class RedirectView(View):
    def get(self, request):
        return render(request, 'dashboard.html')


class Dashboard(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'login_err.html')
        username = request.user.username
        params = {'username' : username}
        params["name"] = "Sprintbiz"
        return render(request, 'dashboard.html', params)

class InvoiceListView(View):
    def get(self, request):
        title ='Invoice List'
        invoice = Invoice_Details.objects.select_related('invoice','service','status').values('invoice_id','invoice__name','hour','service__name','invoice__create_date','invoice__status__name')
        invoice_detail_object = Invoice_Details.objects.filter(invoice__id=Invoice.objects.all())
        return render(request,'invoice.html',{'invoices' : invoice, 'title' : title,})

class InvoicePrintView(View):
    def get(self, request, id):
        invoice_object = Invoice.objects.get(id=id)
        invoice_detail_object = Invoice_Details.objects.filter(invoice_id=id).annotate(service_name=F('service__name')
		                                                       ,price_per_hour=ExpressionWrapper(F('service__price_per_hour'), output_field=FloatField())
															   ,value=ExpressionWrapper(F('service__price_per_hour') * F('hour'), output_field=FloatField())
															   ,tax_value=ExpressionWrapper((F('service__price_per_hour') * F('hour'))*F('service__tax__value')/100, output_field=FloatField())
                                                               ,tax_prct=F('service__tax__value')
															   ,gross_value=ExpressionWrapper((F('service__price_per_hour') * F('hour'))+(F('service__price_per_hour') * F('hour'))*F('service__tax__value')/100, output_field=FloatField())
															   )
        invoice_total = Invoice_Details.objects.filter(invoice_id=id).aggregate(total_tax=Sum((F('service__price_per_hour') * F('hour'))*F('service__tax__value')/100, output_field=FloatField()),total_net=Sum(F('service__price_per_hour') * F('hour'), output_field=FloatField()),total_gross=Sum((F('service__price_per_hour') * F('hour'))*F('service__tax__value')/100+F('service__price_per_hour') * F('hour'), output_field=FloatField()))
        #return render(request,'invoice_detail.html',{'invoices' : object})
        return render(request,'invoice_print.html',{'invoice_object' : invoice_object,'invoice_detail_object' : invoice_detail_object, 'invoice_total' : invoice_total} )

class InvoiceEditView(View):
    def get(self, request, id):
        action_url ='/invoice/'+id+'/edit/'

        invoice = Invoice.objects.get(id=id)
        invoice_form = InvoiceForm(instance=invoice)

        Invoiceformset = inlineformset_factory(Invoice, Invoice_Details, form=InvoiceDetailForm, extra=0)
        formset = Invoiceformset(instance=invoice)
        if request.method == "POST":
            invoice_form = InvoiceForm(request.POST, instance=invoice)
            formset = Invoiceformset(request.POST, instance=invoice)
            if invoice_form.is_valid():
                invoice_instance = invoice_form.save(commit=False)
                formset = Invoiceformset(request.POST, request.FILES, instance=invoice_instance)
                if formset.is_valid():
                    invoice_instance.save()
                    formset.save()
        return render(request, 'invoice_create.html', { 'invoice' : invoice_form,'formset' : formset, 'action_url' : action_url,})

    def post(self, request, id):
        action_url ='/invoice/'+id+'/edit/'

        invoice = Invoice.objects.get(id=id)
        invoice_form = InvoiceForm(instance=invoice)

        Invoiceformset = inlineformset_factory(Invoice, Invoice_Details, form=InvoiceDetailForm, extra=0)
        formset = Invoiceformset(instance=invoice)
        if request.method == "POST":
            invoice_form = InvoiceForm(request.POST, instance=invoice)
            formset = Invoiceformset(request.POST, instance=invoice)
            if invoice_form.is_valid():
                invoice_instance = invoice_form.save(commit=False)
                formset = Invoiceformset(request.POST, request.FILES, instance=invoice_instance)
                if formset.is_valid():
                    invoice_instance.save()
                    formset.save()
        return render(request, 'invoice_create.html', { 'invoice' : invoice_form,'formset' : formset, 'action_url' : action_url,})

class CreateInvoiceView(View):
    def get(self, request):
        action_url = '/invoice/new/'
        invoice_form = InvoiceForm()
        Invoiceformset = inlineformset_factory(Invoice, Invoice_Details, form=InvoiceDetailForm, extra=0)
        detail_formset = Invoiceformset(queryset=Invoice_Details.objects.none())
        return render(request,'invoice_create.html',{'invoice' : invoice_form,'formset' : detail_formset, 'action_url' : action_url,})

    def post(self, request, ):

        invoice_form = InvoiceForm(request.POST)
        Invoiceformset = inlineformset_factory(Invoice, Invoice_Details, form=InvoiceDetailForm, extra=0)
        formset = Invoiceformset(request.POST)
        if request.method == "POST":
            invoice_form = InvoiceForm(request.POST)
            formset = Invoiceformset(request.POST)
            if invoice_form.is_valid():
                invoice_instance = invoice_form.save(commit=False)
                formset = Invoiceformset(request.POST, request.FILES, instance=invoice_instance)
                if formset.is_valid():
                    invoice_instance.save()
                    formset.save()
        action_url = '/invoice/' + str(invoice_instance.pk) + '/edit/'
        print_url = '/invoice/' + str(invoice_instance.pk) + '/print/'
        return render(request, 'invoice_create.html', { 'invoice' : invoice_form,'formset' : formset, 'action_url' : action_url, 'print_url' : print_url,})

class InvoiceSaveView(View):
    def post(self, request,id):
        invoice_records = Invoice.objects.get(id=id)
        Invoiceformset = inlineformset_factory(Invoice, Invoice_Details, form=InvoiceDetailForm, extra=0,)
        invoice_form = InvoiceForm(request.POST)
        invoice_form_obj = invoice_form.save()
        formset = Invoiceformset(request.POST )
        for form in formset:
            form_obj = form.save(commit=False)
            form_obj.invoice_id = invoice_form_obj.id
            form_obj.save()
        return render(request,'invoice_create.html',{'invoice' : invoice_form,'formset' : formset,})

class NewInvoiceSaveView(View):
    def post(self, request):
        invoice_form = InvoiceForm(request.POST)
        formset =Invoiceformset(request.POST, )
        if invoice_form.is_valid():
            if formset.is_valid():
                invoice_form_obj =invoice_form.save()
                for form in formset:
                    form_obj = form.save(commit=False)
                    form_obj.invoice_id = invoice_form_obj.id
                    form_obj.save()
        return render(request,'invoice_create.html',{'invoice' : invoice_form,'formset' : formset,})

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
