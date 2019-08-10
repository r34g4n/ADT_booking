from dal import autocomplete
from django.utils import timezone
from django import forms
from .models import (
    Session,
    Service,
    SessionStatus,
    CancelledSession,
)
from payments.models import (
    PaymentType,
)
from payments.searches import get_conservative_unclaimed_payments
from users.models import Patient, Doctor
from bookings.models import Session, DEFAULT_DIAGNOSIS

from .fields import ListTextWidget, CustomDateWidget

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


patients_list = Patient.objects.all()
services_choices = Service.objects.all()
doctors_list = Doctor.objects.all()
payment_type_list = PaymentType.objects.all()

PAYMENT_choice = (
    ('', '*---select---*'),
    ('1', 'Create New Payment'),
    ('2', 'Claim Posted Payment'),
)


class NewSessionStep1Form(forms.Form):

    patient = forms.ModelChoiceField(
        patients_list,
        widget=autocomplete.ModelSelect2(url='users:patient_autocomplete'),
        help_text="Search Patient by phone number, First or Last name"
    )


class NewSessionStep2Form(forms.Form):

    start_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )

    service = forms.ModelChoiceField(services_choices)
    doctor = forms.ModelChoiceField(doctors_list)
    diagnosis = forms.Field(widget=forms.Textarea, initial=DEFAULT_DIAGNOSIS)
    payment_choice = forms.ChoiceField(choices=PAYMENT_choice, required=True)

    def clean_start_date(self):
        if self.cleaned_data['start_date'] < timezone.now().date():
            raise forms.ValidationError("INVALID DATE. You cannot create or recreate past bookings")
        return self.cleaned_data['start_date']

    def clean_payment_choice(self):
        if self.cleaned_data['payment_choice'] not in ('1', '2'):
            raise forms.ValidationError("INVALID payment choice. Try again!")
        return self.cleaned_data['payment_choice']


class NewSessionStep3NewPaymentForm(forms.Form):
    payment_type = forms.ModelChoiceField(payment_type_list)
    date_of_payment = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    amount = forms.DecimalField(
        max_digits=18,
        decimal_places=2,
        min_value=0.50
    )

    def clean_date_of_payment(self):
        if self.cleaned_data['date_of_payment'] > timezone.now().date():
            raise forms.ValidationError("INVALID DATE of payment. FUTURE payments CANNOT be created")
        return self.cleaned_data['date_of_payment']