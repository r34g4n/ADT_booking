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
from bookings.models import DEFAULT_DIAGNOSIS

from .fields import ListTextWidget, CustomDateWidget

from crispy_forms.layout import Layout, Submit, Row, Column


patients_list = Patient.objects.all()
services_choices = Service.objects.all()
payment_types_list = PaymentType.objects.all()
doctors_list = Doctor.objects.all()


class NewSessionForm(forms.Form):

    patient = forms.CharField(required=True, help_text="search <a href='/'>Patient</a>")
    service = forms.ModelChoiceField(queryset=Service.objects.all(),
                                     required=True
                                     )
    doctor = forms.CharField(required=True)
    diagnosis = forms.Field(widget=forms.Textarea, initial="{{ user.username }}")
    start_date = forms.DateField()
    payment_method = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(NewSessionForm, self).__init__(*args, **kwargs)
        self.fields['patient'].widget = ListTextWidget(data_list=patients_list, name='patients-list')
        self.fields['payment_method'].widget = ListTextWidget(data_list=payment_types_list, name='payment-types-list')
        self.fields['doctor'].widget = ListTextWidget(data_list=doctors_list, name='doctors-list')
        self.fields['start_date'].widget = CustomDateWidget()

