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
from users.models import Patient, Doctor
from bookings.models import Session, DEFAULT_DIAGNOSIS

from .fields import ListTextWidget, CustomDateWidget

from crispy_forms.layout import Layout, Submit, Row, Column


patients_list = Patient.objects.all()
services_choices = Service.objects.all()
doctors_list = Doctor.objects.all()


class NewSessionForm(forms.Form):

    patient = forms.ModelChoiceField(patients_list)
    service = forms.ModelChoiceField(queryset=Service.objects.all(),
                                     required=True
                                     )
    doctor = forms.ModelChoiceField(doctors_list)
    diagnosis = forms.Field(widget=forms.Textarea, initial=DEFAULT_DIAGNOSIS)
    start_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    payment_method = forms.ModelChoiceField(queryset=PaymentType.objects.all())

    def clean_start_date(self):
        if self.cleaned_data['start_date'] < timezone.now().date():
            raise forms.ValidationError("Invalid date. Form cannot be in the past")
        return self.cleaned_data['start_date']


class SessionModelForm(forms.ModelForm):

    def clean_start_date(self):
        if self.cleaned_data['start_date'] < timezone.now().date():
            raise forms.ValidationError("Invalid date value. Past dates cannot be accepted")
        return self.cleaned_data['start_date']

    class Meta:
        model = Session
        fields = "__all__"

