from django.db import models

# Create your models here.

default_email = 'none@none.none'


class Gender(models.Model):
    name = models.CharField(max_length=10, unique=True, editable=False)

    def __str__(self):
        return self.name


class Patient(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=12)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    email = models.EmailField(default=default_email, blank=True)
    uhid = models.BigIntegerField(unique=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Doctor(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=12, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    email = models.EmailField(default=default_email, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
