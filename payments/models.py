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
        return f"{DENOM}{str(self.amount)}{DENOM_CLOSER} ({str(self.date)}) {self.__class__.__name__}"


class InsurancePayment(Payment):
    company = models.ForeignKey(InsuranceCompany, on_delete=models.PROTECT, default=1)
    type = models.ForeignKey(PaymentType, on_delete=models.PROTECT, default=3, editable=False)
    history = HistoricalRecords()

    def __str__(self):
        return f"{DENOM}{str(self.amount)}{DENOM_CLOSER} ({self.date}, {self.company})"


class CashPayment(Payment):
    type = models.ForeignKey(PaymentType, on_delete=models.PROTECT, default=2, editable=False)
    history = HistoricalRecords()


class MobileBankingPayment(Payment):
    mobile_banking_type = models.ForeignKey(MobileBankingType, on_delete=models.PROTECT)
    code = models.CharField(max_length=20)
    type = models.ForeignKey(PaymentType, on_delete=models.PROTECT, default=4, editable=False)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.mobile_banking_type} - {DENOM}{self.amount}{DENOM_CLOSER} - {self.date} - {self.code}"
