from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

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


class InsuranceCompany(models.Model):
    name = models.CharField(max_length=20)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Payment(models.Model):
    date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    patient = models.ForeignKey('users.Patient', on_delete=models.PROTECT)
    history = HistoricalRecords()

    def __str__(self):
        return f"{DENOM}{str(self.amount)}{DENOM_CLOSER} ({str(self.date)})"


class InsurancePayment(Payment):
    company = models.ForeignKey(InsuranceCompany, on_delete=models.PROTECT, default=1)
    history = HistoricalRecords()

    @property
    def type(self):
        return PaymentType.objects.get(pk=3)

    def __str__(self):
        return f"{DENOM}{str(self.amount)}{DENOM_CLOSER} ({self.date}, {self.company}) {self.type}"


class CashPayment(Payment):
    history = HistoricalRecords()

    @property
    def type(self):
        return PaymentType.objects.get(pk=2)

    def __str__(self):
        return f"{DENOM}{str(self.amount)}{DENOM_CLOSER} ({str(self.date)}) {self.type}"


class MobileBankingPayment(Payment):
    mobile_banking_type = models.ForeignKey(MobileBankingType, on_delete=models.PROTECT)
    code = models.CharField(max_length=20, unique_for_month=True)
    history = HistoricalRecords()

    @property
    def type(self):
        return PaymentType.objects.get(pk=4)

    def __str__(self):
        return f"{self.mobile_banking_type} - {DENOM}{self.amount}{DENOM_CLOSER} - {self.date} - {self.code} - {self.type}"
