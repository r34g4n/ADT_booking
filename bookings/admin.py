from django.contrib import admin
from .models import Service, SessionStatus, Session, CancelledSession

# Register your models here.
admin.site.register(Service)
admin.site.register(SessionStatus)
admin.site.register(Session)
admin.site.register(CancelledSession)
