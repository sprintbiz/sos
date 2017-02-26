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
from sos.views import CustomerDetail, CustomerEdit, CustomerDelete, CustomerCreate, CustomerList, TaxDetail, TaxDelete, TaxList, TaxCreate, TaxEdit, JsonDaysNotFilled, EventEdit, EventCreate, EventList, JsonProject, CalendarResponce, RedirectView, Dashboard, InvoiceListView, InvoicePrintView, CreateInvoiceView, InvoiceEditView, NewInvoiceSaveView,InvoiceSaveView,TimescheetView
admin.autodiscover()
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls import include, url

urlpatterns = [
    url(r'^dashboard/$', Dashboard.as_view(), name='dashboard'),
    url(r'^invoice/$', InvoiceListView.as_view(), name='invoice-list'),
    url(r'^invoice/([0-9]+)/edit/$', InvoiceEditView.as_view(), name='invoice-edit'),
    url(r'^invoice/([0-9]+)/print/$', InvoicePrintView.as_view(), name='invoice-print'),
    url(r'^invoice/([0-9]+)/save/$', InvoiceSaveView.as_view(), name='invoice-save'),
	url(r'^invoice/new/$', CreateInvoiceView.as_view()),
    url(r'^invoice/new/save/$', CreateInvoiceView.as_view()),
    url(r'^calendar/$', TimescheetView.as_view()),
    url(r'^event/$', EventList.as_view() , name='event_list'),
    url(r'^event/add/$', EventCreate.as_view()),
    url(r'^event/edit/(?P<id>\w+)/$', EventEdit.as_view()),
    url(r'^calendar/json/event/$', CalendarResponce.as_view()),
    url(r'^json/daysnotfilled/$', JsonDaysNotFilled.as_view()),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^calendar/json/project/$', JsonProject.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tax/$', TaxList.as_view(), name='tax-list'),
    url(r'^tax/create/$', TaxCreate.as_view(), name='tax-create'),
    url(r'^tax/edit/(?P<pk>\w+)/$', TaxEdit.as_view(), name='tax-edit'),
    url(r'^tax/delete/(?P<pk>\w+)/$', TaxDelete.as_view(), name='tax-delete'),
    url(r'^tax/detail/(?P<pk>\w+)/$', TaxDetail.as_view(), name='tax-detail'),
    url(r'^customer/$', CustomerList.as_view(), name='customer-list'),
    url(r'^customer/create/$', CustomerCreate.as_view(), name='customer-create'),
    url(r'^customer/edit/(?P<pk>\w+)/$', CustomerEdit.as_view(), name='customer-edit'),
    url(r'^customer/delete/(?P<pk>\w+)/$', CustomerDelete.as_view(), name='customer-delete'),
    url(r'^customer/detail/(?P<pk>\w+)/$', CustomerDetail.as_view(), name='customer-detail'),
    url(r'^.*$', RedirectView.as_view(), name='home'),
]
