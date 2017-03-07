from django.contrib import admin
from .models import Status
from .models import Tax
from .models import Service
from .models import Organization
from .models import Invoice
from .models import Invoice_Details
from .models import Project
from .models import Event

admin.site.register(Status)
admin.site.register(Tax)
admin.site.register(Service)
admin.site.register(Organization)
admin.site.register(Invoice)
admin.site.register(Project)
admin.site.register(Event)
