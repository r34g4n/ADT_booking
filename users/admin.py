from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Gender, Patient, Doctor

# Register your models here.
admin.site.register(Gender, SimpleHistoryAdmin)
admin.site.register(Patient, SimpleHistoryAdmin)
admin.site.register(Doctor, SimpleHistoryAdmin)
