from django.contrib import admin
from .models import (
    Service,
    SessionStatus,
    Session,
    BedType,
    Location,
    BookingType,
    CancelledSession
)
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
admin.site.register(Service, SimpleHistoryAdmin)
admin.site.register(SessionStatus, SimpleHistoryAdmin)
admin.site.register(CancelledSession, SimpleHistoryAdmin)
admin.site.register(BedType)
admin.site.register(Location)
admin.site.register(BookingType)


@admin.register(Session)
class SessionAdmin(SimpleHistoryAdmin):
    fieldsets = [
        (None, {'fields': ['patient']}),
        ('Booking Detail', {
            'fields': [
                'service', 'start_date', 'end_date', 'status', 'booking_type', 'location', 'bed_type', 'doctor'
            ]
        }),
        ('Diagnosis', {'fields': ['doctor_diagnosis']}),
        ('Payment Info', {
            'fields': [
                'payment'
            ]
        }),
        ('Other', {
            'fields': ['remarks']
        })
    ]
    list_display = ('patient', 'service', 'location', 'doctor', 'start_date', 'end_date', 'status', 'timeline')
    search_fields = ['patient__first_name', 'patient__middle_name', 'patient__last_name']
    list_filter = ['status', 'start_date', 'end_date', 'service', 'location',]
