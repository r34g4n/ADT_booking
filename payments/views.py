from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import (
    UndefinedPaymentMethod,
    CashPayment,
    InsurancePayment,
    MobileBankingPayment,
    CorporatePayment
)
from .forms import (
    ChoosePaymentForm,
    CashPaymentModelForm,
    UndefinedPaymentModelForm,
    InsurancePaymentModelForm,
    MobileBankingPaymentModelForm,
    CorporatePaymentModelForm
)
from django.views.generic import (
    ListView,
    UpdateView,
    DetailView,
    CreateView
)

PAYMENT_UTILITY_FORMS = {
    'choose': ChoosePaymentForm,
    'Undefined*': (UndefinedPaymentMethod, UndefinedPaymentModelForm),
    'Cash': (CashPayment, CashPaymentModelForm),
    'Insurance': (InsurancePayment, InsurancePaymentModelForm),
    'Mobile Banking': (MobileBankingPayment, MobileBankingPaymentModelForm),
    'Corporate': (CorporatePayment, CorporatePaymentModelForm)
}


@login_required
def choose_payment_to_post(request):
    context = {
        'title': 'New Payment',
        'submit': 'Next',
        'other_form': PAYMENT_UTILITY_FORMS['choose']
    }
    if request.method == 'POST':
        form = PAYMENT_UTILITY_FORMS['choose'](request.POST)
        print(form.is_valid())
        print(str(form.cleaned_data['payment_type']))
        if form.is_valid():
            choice = form.cleaned_data['payment_type']
            if choice in (None, ChoosePaymentForm):
                messages.warning(request, "Invalid payment choice. Please try again!")
                return redirect('payments:choose_payment_to_post')
            return redirect('payments:create_payment', choice)
    return render(request, 'bookings/bookings_home.html', context)


@login_required
def create_payment(request, *args, **kwargs):
    choice = kwargs.get('choice')
    choice = PAYMENT_UTILITY_FORMS.get(choice, None)
    if choice in (None, ChoosePaymentForm):
        messages.warning(request, "Invalid payment choice. Please try again!")
        return redirect('payments:choose_payment_to_post')
    context = {
        'title': 'Create payment',
        'submit': 'Create'
    }
    if request.method == 'POST':
        form = choice[1](request.POST)
        if form.is_valid():
            context['other_form'] = form
            form.save()
            messages.success(request, f"{choice[0].type} payment has been successfully posted")
            return redirect('bookings:bookings-home')
    context['other_form'] = choice[1]()
    return render(request, 'bookings/bookings_home.html', context)
