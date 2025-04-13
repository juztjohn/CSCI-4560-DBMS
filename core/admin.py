from django.contrib import admin
from .models import Doctor, Lab, Billing

# Register your models here.

admin.site.register(Doctor)
admin.site.register(Lab)
admin.site.register(Billing)