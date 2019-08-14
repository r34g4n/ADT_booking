from django.db import models
from simple_history.models import HistoricalRecords
from django.conf import settings
from django.utils import timezone
import datetime

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
    middle_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=12, unique=True)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT, default=3)
    email = models.EmailField(unique=True, null=True, blank=True)
    uhid = models.BigIntegerField(unique=True, blank=True, null=True)
    history = HistoricalRecords()
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        if self.middle_name:
            return f'{self.first_name} {self.middle_name} {self.last_name}'
        return f'{self.first_name} {self.last_name}'

    @property
    def age(self):
        today = timezone.now().date()
        age = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

        return age

    def __str__(self):
        return self.full_name


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
