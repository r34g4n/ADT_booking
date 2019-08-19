from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from polymorphic.models import PolymorphicModel

# Create your models here.
DENOM = 'KES.'
DENOM_CLOSER = "/="


class PaymentType(models.Model):
    name = models.CharField(max_length=20)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class MobileBankingType(models.Model):
    name = models.CharField(max_length=45, unique=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Corporation(models.Model):
    name = models.CharField(max_length=45, unique=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class InsuranceCompany(models.Model):
    name = models.CharField(max_length=20)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Payment(PolymorphicModel):
    type = None
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    patient = models.ForeignKey('users.Patient', on_delete=models.PROTECT)
    history = HistoricalRecords()

    def __str__(self):
        return f"{DENOM}{str(self.amount)}{DENOM_CLOSER} ({str(self.date)})"

    @property
    def denom(self):
        return DENOM

    @property
    def denom_closer(self):
        return DENOM_CLOSER


class InsurancePayment(Payment):
    type = PaymentType.objects.get(pk=3)
    company = models.ForeignKey(InsuranceCompany, on_delete=models.PROTECT, default=1)
    history = HistoricalRecords()

    @property
    def additional_info(self):
        return self.company


class CorporatePayment(Payment):
    type = PaymentType.objects.get(pk=5)
    corporation = models.ForeignKey(Corporation, on_delete=models.PROTECT)
    history = HistoricalRecords()

    @property
    def additional_info(self):
        return self.corporation


class UndefinedPaymentMethod(Payment):
    type = PaymentType.objects.get(pk=1)
    history = HistoricalRecords()

    @property
    def additional_info(self):
        return "Hybrid of payments"


class CashPayment(Payment):
    type = PaymentType.objects.get(pk=2)
    history = HistoricalRecords()

    @property
    def additional_info(self):
        return "..."


class MobileBankingPayment(Payment):
    type = PaymentType.objects.get(pk=4)
    mobile_banking_type = models.ForeignKey(MobileBankingType, on_delete=models.PROTECT, default=1)
    code = models.CharField(max_length=20, unique=True)
    history = HistoricalRecords()

    @property
    def additional_info(self):
        return f"{self.mobile_banking_type}({self.code.upper()})"
