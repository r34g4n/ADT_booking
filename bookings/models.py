from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

# Create your models here.


class Service(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=100, default="Service. No further description provided")
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class SessionStatus(models.Model):
    status = models.CharField(max_length=10, editable=False)
    indicator = models.CharField(max_length=10)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = 'Session Statuses'

    def __str__(self):
        return self.status


class Session(models.Model):
    patient = models.ForeignKey('users.Patient', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    doctor = models.ForeignKey('users.Doctor', on_delete=models.PROTECT)
    doctor_diagnosis = models.TextField(max_length=200)
    start_date = models.DateField(default=timezone.now)
    payment = models.ForeignKey('payments.Payment', on_delete=models.CASCADE)
    status = models.ForeignKey(SessionStatus, on_delete=models.PROTECT, default=1)
    remarks = models.TextField(max_length=200)
    history = HistoricalRecords()
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class CancelledSession(models.Model):
    session = models.ForeignKey(Session, on_delete=models.PROTECT)
    reason_for_cancelling = models.TextField(max_length=100)
    history = HistoricalRecords()
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
