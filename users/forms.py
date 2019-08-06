from django import forms
from .models import Patient, DEFAULT_EMAIL

# crispy-forms import
from crispy_forms.layout import Layout, Submit, Row, Column


class PatientRegistrationForm(forms.ModelForm):

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number', None)
        if phone_number.isdigit():
            return phone_number
        else:
            raise forms.ValidationError("Invalid Phone number. Please Try again!")

    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        qs = Patient.objects.filter(email=email)
        if len(qs) == 0 or qs.first().email == DEFAULT_EMAIL:
            return email
        else:
            raise forms.ValidationError("A Patient with similar email already exists.\n"
                                        "This could be a duplicate.\n"
                                        "Kindly confirm before proceeding")

    class Meta:
        model = Patient
        fields = "__all__"
