from django.db import models
from django.utils import timezone

# Create your models here.
DENOM = 'KES.'
DENOM_CLOSER = "/="


class MobileBankingType(models.Model):
    name = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    patient = models.ForeignKey('users.Patient', on_delete=models.PROTECT)

    def __str__(self):
        return f"{DENOM}{str(self.amount)}{DENOM_CLOSER} ({str(self.date)}) {self.__class__.__name__}"


class InsurancePayment(Payment):
    company = models.CharField(max_length=20)

    def __str__(self):
        return f"{DENOM}{str(self.amount)}{DENOM_CLOSER} ({self.date}, {self.company})"


class CashPayment(Payment):
    pass


class MobileBankingPayment(Payment):
    mobile_banking_type = models.ForeignKey(MobileBankingType, on_delete=models.PROTECT)
    code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.mobile_banking_type} - {DENOM}{self.amount}{DENOM_CLOSER} - {self.date} - {self.code}"
