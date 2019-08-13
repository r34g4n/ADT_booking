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
admin.site.register(Session, SimpleHistoryAdmin)
admin.site.register(CancelledSession, SimpleHistoryAdmin)
admin.site.register(BedType)
admin.site.register(Location)
admin.site.register(BookingType)
