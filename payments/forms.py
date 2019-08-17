from django.contrib.auth.models import User
from django.utils import timezone
from .models import (
    InsuranceCompany,
    MobileBankingType,
    MobileBankingPayment,
    InsurancePayment,
    Payment,
    Corporation
)
from .models import (
    PaymentType,
    CashPayment,
    UndefinedPaymentMethod,
    InsurancePayment,
    MobileBankingPayment,
    CorporatePayment
)
from django import forms
from dal import autocomplete
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


EXTRA_TAGS_FOR_CASH_OR_UNDEFINED_PAYMENTS = "No extra tags needed because the" \
                                            " payment is either: " \
                                            "\n\t-Cash" \
                                            "\n\t-Undefined*" \
                                            "\n or" \
                                            "\n\t-Unclaimed"


class CashOrUndefinedPaymentForm(forms.Form):
    extra_tags = forms.Field(
        widget=forms.Textarea(attrs={
            'rows': '5',
            'class': 'font-weight-bold'
        }),
        initial=EXTRA_TAGS_FOR_CASH_OR_UNDEFINED_PAYMENTS,
        disabled=True
    )
    remarks = forms.Field(
        widget=forms.Textarea(attrs={
            'rows': '5'
        }),
        label="Bookings remarks(if any)",
        required=False
    )


class CorporatePaymentForm(forms.Form):

    corporation = forms.ModelChoiceField(Corporation.objects.all())
    remarks = forms.Field(
        widget=forms.Textarea(attrs={
            'rows': '5'
        }),
        label="Bookings remarks(if any)",
        required=False
    )


class InsurancePaymentForm(forms.Form):

    company = forms.ModelChoiceField(
        InsuranceCompany.objects.all(),
        label="Insurance Company"
    )
    remarks = forms.Field(
        widget=forms.Textarea(attrs={
            'rows': '5'
        }),
        label="Bookings remarks(if any)",
        required=False
    )


class MobilePaymentForm(forms.Form):
    mobile_banking_type = forms.ModelChoiceField(
        MobileBankingType.objects.all()
    )

    code = forms.Field(
        widget=forms.TextInput(attrs={
            'maxlength': '20'
        })
    )
    remarks = forms.Field(
        widget=forms.Textarea(attrs={
            'rows': '5'
        }),
        label="Bookings remarks(if any)",
        required=False
    )

    def clean_code(self):
        exists = MobileBankingPayment.objects.filter(code=self.cleaned_data['code'])
        mobile_banking_type = self.cleaned_data['mobile_banking_type']
        if exists:
            raise forms.ValidationError(
                f"An {mobile_banking_type} payment with this code already exists"
            )
        return self.cleaned_data['code']


class CashPaymentModelForm(forms.ModelForm):
    class Meta:
        model=CashPayment
        fields="__all__"
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date'
            }),
            'patient': autocomplete.ModelSelect2(url='users:patient_autocomplete')
        }
        help_texts = {
            'patient': 'Search Patient by phone number or name'
        }
        labels = {
            'patient': "Patient's Name"
        }


class UndefinedPaymentModelForm(forms.ModelForm):
    class Meta:
        model = UndefinedPaymentMethod
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date'
            }),
            'patient': autocomplete.ModelSelect2(url='users:patient_autocomplete')
        }
        help_texts = {
            'patient': 'Search Patient by phone number or name'
        }
        labels = {
            'patient': "Patient's Name"
        }


class InsurancePaymentModelForm(forms.ModelForm):
    class Meta:
        model = InsurancePayment
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date'
            }),
            'patient': autocomplete.ModelSelect2(url='users:patient_autocomplete')
        }
        help_texts = {
            'patient': 'Search Patient by phone number or name'
        }
        labels = {
            'patient': "Patient's Name"
        }


class MobileBankingPaymentModelForm(forms.ModelForm):

    class Meta:
        model = MobileBankingPayment
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date'
            }),
            'patient': autocomplete.ModelSelect2(url='users:patient_autocomplete')
        }
        help_texts = {
            'patient': 'Search Patient by phone number or name'
        }
        labels = {
            'patient': "Patient's Name"
        }


class CorporatePaymentModelForm(forms.ModelForm):

    class Meta:
        model = CorporatePayment
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date'
            }),
            'patient': autocomplete.ModelSelect2(url='users:patient_autocomplete')
        }
        help_texts = {
            'patient': 'Search Patient by phone number or name'
        }
        labels = {
            'patient': "Patient's Name"
        }


class ChoosePaymentForm(forms.Form):

    payment_type = forms.ModelChoiceField(
        PaymentType.objects.all(),
        help_text="Choose payment type from the dropdown"
    )

