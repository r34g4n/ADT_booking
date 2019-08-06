from django.db import models
from simple_history.models import HistoricalRecords
from django.conf import settings

# Create your models here.

DEFAULT_EMAIL = 'none@none.none'


class Gender(models.Model):
    name = models.CharField(max_length=10, unique=True, editable=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    @property
    def initial(self):
        if self.name == 'Other*':
            return '*'
        return self.name[0].upper()


class Patient(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=12, unique=True)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT, default=3)
    email = models.EmailField(default=DEFAULT_EMAIL)
    uhid = models.BigIntegerField(unique=True, null=True)
    history = HistoricalRecords()
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Doctor(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=12)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    email = models.EmailField(default=DEFAULT_EMAIL, null=True)
    history = HistoricalRecords()
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
