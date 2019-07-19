from django.contrib import admin
from .models import MobileBankingType, Payment, MobileBankingPayment, InsurancePayment, CashPayment

# Register your models here.
admin.site.register(MobileBankingType)
admin.site.register(Payment)
admin.site.register(MobileBankingPayment)
admin.site.register(InsurancePayment)
admin.site.register(CashPayment)