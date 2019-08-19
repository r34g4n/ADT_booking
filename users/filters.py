from .models import Patient, Gender
from django.db.models import Q
from django.utils import timezone
from bookings.models import Session

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


def patient_list_unfiltered():
    return Patient.objects.all()


def patient_list_root(*args, **kwargs):
    if args:
        kwargs = args[0]
    registered_from_date = kwargs.get('registered_from_date', None)
    to = kwargs.get('to', None)
    gender = kwargs.get('gender', None)

    sort_by = kwargs.get('sort_by', None)
    sort_by = SORT_BY_DICT.get(sort_by, None)

    patients = patient_list_unfiltered()

    if kwargs:
        print("kwargs -- ", kwargs)
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
    print("args --  ", args)
    print("kwargs -- ", kwargs)
    if args:
        kwargs = args[0]
    filter_params = kwargs
    sort_by = filter_params.get('sort_by', None)
    sort_by = SORT_BY_DICT2.get(sort_by, None)
    print('filter_params---filter__params')
    filter_params['sort_by'] = sort_by
    for key, value in filter_params.items():
        if value is not None:
            print(f"{key} -- {value}")

    bookings_list = booking_list_unfiltered()

    for key, value in filter_params.items():
        if value is not None:
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
                for session in bookings_list:
                    print(session.patient)
    return bookings_list
