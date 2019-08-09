from .models import Payment
from bookings.models import Session
from users.models import Patient


def get_conservative_unclaimed_payments(patient_pk):
    booking_payments_pks = [booking.payment.pk for booking in Session.objects.all()]
    conservative_unclaimed_payments = Payment.objects.filter(patient_id=patient_pk).exclude(pk__in=booking_payments_pks)
    return conservative_unclaimed_payments


def all_unclaimed_payments():
    booking_payments_pks = [booking.payment.pk for booking in Session.objects.all()]
    conservative_unclaimed_payments = Payment.objects.all().exclude(pk__in=booking_payments_pks)
    return conservative_unclaimed_payments
