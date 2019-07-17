from django.contrib import admin
from .models import Gender, Patient, Doctor

# Register your models here.

admin.site.register(Gender)
admin.site.register(Patient)
admin.site.register(Doctor)