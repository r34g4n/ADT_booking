from .models import Patient, Gender
from django.db.models import Q
from django.utils import timezone
from bookings.models import Session
from payments.models import (
    Payment,
    UndefinedPaymentMethod,
    CashPayment,
    InsurancePayment,
    MobileBankingPayment,
    CorporatePayment
)

SORT_BY_DICT = {
    'registration_date_desc': '-date_added',
    'registration_date_asc': 'date_added',
    'name_asc': 'first_name',
    'name_desc': '-first_name'
}

SORT_BY_DICT2 = {
    'start_date_desc': '-start_date',
    'start_date_asc': 'start_date',
    'name_asc': 'patient__first_name',
    'name_desc': '-patient__first_name',
    'end_date_desc': '-end_date',
    'end_date_asc': 'end_date',
}

PAYMENT_SORT_BY = {
    'date_desc': '-date',
    'date_asc': 'date',
    'amount_desc': '-amount',
    'amount_asc': 'amount',
    'name_asc': '-patient__first_name',
    'name_desc': 'patient__first_name'
}

PAYMENT_TYPE = {
    1: UndefinedPaymentMethod,
    2: CashPayment,
    3: InsurancePayment,
    4: MobileBankingPayment,
    5: CorporatePayment
}


def patient_list_unfiltered():
    return Patient.objects.all()


def patient_list_root(*args, **kwargs):
    if args:
        kwargs = args[0]
    else:
        patients = Patient.objects.all()[:50]
        return patients
    registered_from_date = kwargs.get('registered_from_date', None)
    to = kwargs.get('to', None)
    gender = kwargs.get('gender', None)

    sort_by = kwargs.get('sort_by', None)
    sort_by = SORT_BY_DICT.get(sort_by, None)

    patients = patient_list_unfiltered()

    if kwargs:
        if registered_from_date == to and to is not None:
            patients = patients.filter(date_added=registered_from_date)
        else:
            if registered_from_date:
                patients = patients.filter(date_added__gte=registered_from_date)
            else:
                pass
            if to:
                patients = patients.filter(date_added__lte=to)
        if gender:
            patients = patients.filter(gender=gender)
        if sort_by:
            patients = patients.order_by(sort_by)
    return patients


def booking_list_unfiltered():
    return Session.objects.all()


def bookings_list_root(*args, **kwargs):
    if args:
        kwargs = args[0]
    else:
        booking_list = Session.objects.all()[:50]
        return booking_list
    filter_params = kwargs
    sort_by = filter_params.get('sort_by', None)
    sort_by = SORT_BY_DICT2.get(sort_by, None)
    filter_params['sort_by'] = sort_by

    bookings_list = booking_list_unfiltered()

    for key, value in filter_params.items():
        if value is not None:
            if key == 'patient':
                bookings_list = bookings_list.filter(patient=value)
            if key == 'status':
                bookings_list = bookings_list.filter(status=value)
            if key == 'gender':
                bookings_list = bookings_list.filter(patient__gender=value)
            if key == 'service':
                bookings_list = bookings_list.filter(service=value)
            if key == 'location':
                bookings_list =  bookings_list.filter(location=value)
            if key == 'doctor':
                bookings_list = bookings_list.filter(doctor=value)
            if key == 'from_date':
                bookings_list = bookings_list.filter(start_date__gte=value)
            if key == 'to_date':
                bookings_list = bookings_list.filter(start_date__lte=value)
            if key == 'sort_by':
                bookings_list = bookings_list.order_by(sort_by)
    if filter_params.get('timeline'):
        bookings_list = [session for session in bookings_list if session.timeline == filter_params.get('timeline')]
    return bookings_list


def payment_list_unfiltered():
    return Payment.objects.all()


def payment_list_root(*args, **kwargs):
    if args:
        kwargs = args[0]
    filter_params = kwargs
    sort_by = filter_params.get('sort_by', None)
    sort_by = PAYMENT_SORT_BY.get(sort_by, None)
    if not args and not kwargs:
        payment_list = Payment.objects.all()[:50]
        return payment_list

    BLACK_LIST = (None)

    if filter_params.get('type', None):
        print("cba")
        payment_type = PAYMENT_TYPE.get(filter_params['type'].pk)
        payment_list = Payment.objects.instance_of(payment_type)
    else:
        payment_list = payment_list_unfiltered()
    for key, value in filter_params.items():
        if value:
            if key == 'patient':
                payment_list = payment_list.filter(patient__pk=value.pk)
            if key == 'from_date':
                payment_list = payment_list.filter(date__gte=value)
            if key == 'to_date':
                payment_list = payment_list.filter(date__lte=value)
            if key == 'from_amount':
                payment_list = payment_list.filter(amount__gte=value)
            if key == 'to_amount':
                payment_list = payment_list.filter(amount__lte=value)
            if key == 'sort_by':
                payment_list = payment_list.order_by(sort_by)
    if filter_params.get('extra_tags', None):
        extra_tags = filter_params['extra_tags']
        payment_list = [pay for pay in payment_list if extra_tags.upper() in str(pay.get_real_instance().additional_info).upper()]
    return payment_list
