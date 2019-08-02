from django.contrib import admin
from .models import MobileBankingType, Payment, MobileBankingPayment, InsurancePayment, CashPayment
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
admin.site.register(MobileBankingType)

admin.site.register(Payment, SimpleHistoryAdmin)
admin.site.register(CashPayment, SimpleHistoryAdmin)
admin.site.register(MobileBankingPayment, SimpleHistoryAdmin)
admin.site.register(InsurancePayment, SimpleHistoryAdmin)