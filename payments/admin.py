from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from .models import MobileBankingType, Payment, MobileBankingPayment, InsurancePayment, CashPayment, UndefinedPaymentMethod
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
admin.site.register(MobileBankingType)

"""admin.site.register(Payment, SimpleHistoryAdmin)"""
admin.site.register(CashPayment, SimpleHistoryAdmin)
admin.site.register(MobileBankingPayment, SimpleHistoryAdmin)
admin.site.register(InsurancePayment, SimpleHistoryAdmin)
admin.site.register(UndefinedPaymentMethod, SimpleHistoryAdmin)


@admin.register(Payment)
class PaymentAdmin(SimpleHistoryAdmin, PolymorphicParentModelAdmin):
    base_model = Payment
    child_models = (InsurancePayment, CashPayment, MobileBankingPayment, UndefinedPaymentMethod)