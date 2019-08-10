from django.contrib.auth.models import User
from django.utils import timezone
from .models import MobileBankingType, MobileBankingPayment, Payment
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class NewPaymentForm(forms.ModelForm):

    pass


class NewCashPayment(NewPaymentForm):
    pass


class NewInsurancePayment(NewPaymentForm):
    pass


class NewMobilePayment(NewPaymentForm):
    mobile_banking_type = forms.ModelChoiceField(MobileBankingType.objects.all())
    code = forms.CharField(max_length=20)


class MobilePaymentModelForm(forms.ModelForm):
    pass
