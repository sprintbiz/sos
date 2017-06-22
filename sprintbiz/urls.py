"""my_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from sos.views import ProjectCreate, ProjectDelete, ProjectDetail, ProjectEdit, ProjectList, ServiceCreate, ServiceDelete, ServiceDetail, ServiceEdit, ServiceList, ManufacturerList, ManufacturerCreate, MaterialList, MaterialCreate, MaterialDelete, MaterialEdit, MaterialDetail, MaterialGroupCreate, MaterialGroupDelete, MaterialGroupDetail, MaterialGroupEdit, MaterialGroupList, MaterialTransactionDelete, MaterialTransactionEdit, MaterialTransactionList, OrganizationDetail, OrganizationEdit, OrganizationDelete, OrganizationCreate, OrganizationList, TaxDetail, TaxDelete, TaxList, TaxCreate, TaxEdit, JsonDaysNotFilled, EventEdit, EventCreate, EventList, JsonProject, CalendarResponce, RedirectView, Dashboard, InvoiceListView, InvoicePrintView, CreateInvoiceView, InvoiceEditView, TimescheetView, ProfileView, ProfileChangePassword, ProfileCreateView
admin.autodiscover()
from sos.forms import LoginForm
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls import include, url

urlpatterns = [
    url(r'^dashboard/$', Dashboard.as_view(), name='dashboard'),
    url(r'^invoice/(?P<page>\d+)/$', InvoiceListView.as_view(), name='invoice-list-page'),
    url(r'^invoice/$', InvoiceListView.as_view(), name='invoice-list'),
    url(r'^invoice/(?P<pk>\d+)/edit/$', InvoiceEditView.as_view(), name='invoice-edit'),
    url(r'^invoice/([0-9]+)/print/$', InvoicePrintView.as_view(), name='invoice-print'),
	url(r'^invoice/new/$', CreateInvoiceView.as_view(), name='invoice-create'),
    url(r'^invoice/new/save/$', CreateInvoiceView.as_view()),
    url(r'^calendar/$', TimescheetView.as_view()),
    url(r'^event/$', EventList.as_view() , name='event_list'),
    url(r'^event/add/$', EventCreate.as_view()),
    url(r'^event/edit/(?P<id>\w+)/$', EventEdit.as_view()),
    url(r'^calendar/json/event/$', CalendarResponce.as_view()),
    url(r'^json/daysnotfilled/$', JsonDaysNotFilled.as_view()),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html','authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'dashboard'}, name='logout'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^profile/create/$', ProfileCreateView.as_view(), name='profile-create'),
    url(r'^profile/password/change/$', ProfileChangePassword.as_view(), name='profile-password-change'),
    url(r'^profile/password/done/$', auth_views.password_change_done, name='password-change-done'),
    url(r'^calendar/json/project/$', JsonProject.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^manufacturer/$', ManufacturerList.as_view(), name='manufacturer-list'),
    url(r'^manufacturer/create/$', ManufacturerCreate.as_view(), name='manufacturer-create'),
    url(r'^material/$', MaterialList.as_view(), name='material-list'),
    url(r'^material/create/$', MaterialCreate.as_view(), name='material-create'),
    url(r'^material/edit/(?P<pk>\w+)/$', MaterialEdit.as_view(), name='material-edit'),
    url(r'^material/delete/(?P<pk>\w+)/$', MaterialDelete.as_view(), name='material-delete'),
    url(r'^material/detail/(?P<pk>\w+)/$', MaterialDetail.as_view(), name='material-detail'),
    url(r'^material_group/$', MaterialGroupList.as_view(), name='material-group-list'),
    url(r'^material_group/create/$', MaterialGroupCreate.as_view(), name='material-group-create'),
    url(r'^material_group/edit/(?P<pk>\w+)/$', MaterialGroupEdit.as_view(), name='material-group-edit'),
    url(r'^material_group/delete/(?P<pk>\w+)/$', MaterialGroupDelete.as_view(), name='material-group-delete'),
    url(r'^material_group/detail/(?P<pk>\w+)/$', MaterialGroupDetail.as_view(), name='material-group-detail'),
    url(r'^material_transaction/$', MaterialTransactionList.as_view(), name='material-transaction-list'),
    url(r'^material_transaction/delete/(?P<pk>\w+)/$', MaterialTransactionDelete.as_view(), name='material-transaction-delete'),
    url(r'^material_transaction/edit/(?P<pk>\w+)/$', MaterialTransactionEdit.as_view(), name='material-transaction-edit'),
    url(r'^organization/$', OrganizationList.as_view(), name='organization-list'),
    url(r'^organization/create/$', OrganizationCreate.as_view(), name='organization-create'),
    url(r'^organization/edit/(?P<pk>\w+)/$', OrganizationEdit.as_view(), name='organization-edit'),
    url(r'^organization/delete/(?P<pk>\w+)/$', OrganizationDelete.as_view(), name='organization-delete'),
    url(r'^organization/detail/(?P<pk>\w+)/$', OrganizationDetail.as_view(), name='organization-detail'),
    url(r'^project/$', ProjectList.as_view(), name='project-list'),
    url(r'^project/create/$', ProjectCreate.as_view(), name='project-create'),
    url(r'^project/delete/(?P<pk>\w+)/$', ProjectDelete.as_view(), name='project-delete'),
    url(r'^project/detail/(?P<pk>\w+)/$', ProjectDetail.as_view(), name='project-detail'),
    url(r'^project/edit/(?P<pk>\w+)/$', ProjectEdit.as_view(), name='project-edit'),
    url(r'^service/$', ServiceList.as_view(), name='service-list'),
    url(r'^service/create/$', ServiceCreate.as_view(), name='service-create'),
    url(r'^service/delete/(?P<pk>\w+)/$', ServiceDelete.as_view(), name='service-delete'),
    url(r'^service/detail/(?P<pk>\w+)/$', ServiceDetail.as_view(), name='service-detail'),
    url(r'^service/edit/(?P<pk>\w+)/$', ServiceEdit.as_view(), name='service-edit'),
    url(r'^tax/$', TaxList.as_view(), name='tax-list'),
    url(r'^tax/create/$', TaxCreate.as_view(), name='tax-create'),
    url(r'^tax/delete/(?P<pk>\w+)/$', TaxDelete.as_view(), name='tax-delete'),
    url(r'^tax/detail/(?P<pk>\w+)/$', TaxDetail.as_view(), name='tax-detail'),
    url(r'^tax/edit/(?P<pk>\w+)/$', TaxEdit.as_view(), name='tax-edit'),
    url(r'^.*$', RedirectView.as_view(), name='home'),
]
