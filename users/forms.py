from django.forms import ModelForm
from .models import Patient


class PatientRegistrationForm(ModelForm):

    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'gender', 'uhid']
