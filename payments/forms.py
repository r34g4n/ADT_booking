from django.contrib.auth.models import User
from django.utils import timezone
from .models import MobileBankingType, MobileBankingPayment
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class NewPaymentForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(forms.Form, self).__init__(*args, **kwargs)

    date = forms.DateField(
        help_text="Date and time of payment.\n"
        "Time may be an approximate.",
        initial=timezone.now
    )

    amount = forms.DecimalField(
        max_value=499999,
        min_value=99,
        decimal_places=2,
    )
    added_by = forms.ModelChoiceField(
        User.objects.all()
    )

    def clean_added_by(self):
        if self.request is None:
            raise forms.ValidationError("We could not capture your username!"
                                        "Please Try again!")
        if self.cleaned_data['added_by'] != self.request.user.id:
            raise forms.ValidationError("Incorrect username."
                                        "Please input your name in added_by field")
        return self.cleaned_data['added_by']


class NewCashPayment(NewPaymentForm):
    pass


class NewInsurancePayment(NewPaymentForm):
    company = forms.CharField(max_length=20)


class NewMobilePayment(NewPaymentForm):
    mobile_banking_type = forms.ModelChoiceField(MobileBankingType.objects.all())
    code = forms.CharField(max_length=20)


class MobilePaymentModelForm(forms.ModelForm):

    class Meta:
        model = MobileBankingPayment
        fields = ['date', 'amount', 'type', 'code']