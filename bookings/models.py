from django.db import models
from django.urls import reverse
from django.utils import timezone
from simple_history.models import HistoricalRecords

# Create your models here.
DEFAULT_DIAGNOSIS = 'none provided'
DEFAULT_SESSION_STATUS_ID = 2


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
        verbose_name = "Booking Status"
        verbose_name_plural = 'Booking Statuses'

    def __str__(self):
        return self.status


class BookingType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class BedType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


"""DEFAULT_BED_TYPE = BedType.objects.get(pk=1)
DEFAULT_LOCATION = Location.objects.get(pk=1)
DEFAULT_BOOKING_TYPE = BookingType.objects.get(pk=1)"""


class Session(models.Model):
    patient = models.ForeignKey('users.Patient', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    doctor = models.ForeignKey('users.Doctor', on_delete=models.PROTECT)
    doctor_diagnosis = models.TextField(max_length=300, default=DEFAULT_DIAGNOSIS)
    start_date = models.DateField('Admission Date', default=timezone.now)
    end_date = models.DateField('Discharge Date', default=timezone.now)
    payment = models.OneToOneField('payments.Payment', on_delete=models.PROTECT)
    status = models.ForeignKey(SessionStatus, on_delete=models.PROTECT, default=1)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    bed_type = models.ForeignKey(BedType, on_delete=models.PROTECT)
    booking_type = models.ForeignKey(BookingType, on_delete=models.PROTECT)
    remarks = models.TextField(max_length=200, blank=True)
    history = HistoricalRecords()
    date_added = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('bookings:session-detail', kwargs={'pk': self.pk})
    @property
    def is_past(self):
        return self.end_date < timezone.now().date()
    """is_past.admin_order_field = 'start_date'
    is_past.boolean = True
    is_past.short_description = 'Patient Discharged?'"""
    @property
    def timeline(self):
        if self.start_date > self.end_date:
            return "INCONSISTENT"
        if self.is_past:
            return "PAST"
        elif self.start_date <= timezone.now().date() <= self.end_date:
            return "ACTIVE"
        elif self.start_date > timezone.now().date() and self.end_date >= timezone.now().date():
            return "FUTURE"
        else:
            return "INCONSISTENT"
    def __str__(self):
        return f"for {self.patient.full_name}, {self.location}"

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = 'Bookings'


class CancelledSession(models.Model):
    session = models.ForeignKey(Session, on_delete=models.PROTECT)
    reason_for_cancelling = models.TextField(max_length=100)
    history = HistoricalRecords()
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cancelled Booking"
        verbose_name_plural = 'Cancelled Bookings'
