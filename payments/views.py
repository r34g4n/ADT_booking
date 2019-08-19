from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import (
    Payment,
    UndefinedPaymentMethod,
    CashPayment,
    InsurancePayment,
    MobileBankingPayment,
    CorporatePayment
)
from users.models import Patient
from .forms import (
    ChoosePaymentForm,
    CashPaymentModelForm,
    UndefinedPaymentModelForm,
    InsurancePaymentModelForm,
    MobileBankingPaymentModelForm,
    CorporatePaymentModelForm,
)
from bookings.forms import NewSessionStep1Form
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


class PaymentsListView(LoginRequiredMixin, ListView):
    model = Payment
    context_object_name = 'payments'
    ordering = ['-date']
    extra_context = {
        'title': 'View All Payments'
    }
    paginate_by = 20


def payment_update_home(request):
    context = {
        'other_form': NewSessionStep1Form()
    }
    if request.method == 'POST':
        form = NewSessionStep1Form(request.POST)
        if form.is_valid():
            patient = form.cleaned_data['patient']
            return redirect('payments:update_payment', patient.pk)
        context['other_form'] = form
    return render(request, 'bookings/bookings_home.html', context=context)


class PatientPaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'payments/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 10
    extra_context = {
        'edit': True
    }

    def get_queryset(self):
        patient = get_object_or_404(Patient, pk=self.kwargs.get('pk'))
        return Payment.objects.filter(patient=patient).order_by('-date')


class PaymentUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Payment
    template_name = 'payments/payment_form.html'
    success_url = reverse_lazy('payments:view_payment_all')
    extra_context = {
        'title': 'Edit Payment'
    }
    @property
    def success_message(self):
        model_type = self.model.get_real_instance(self.get_object()).type
        return f"{model_type} Payment was successfully updated!"
    @property
    def form_class(self):
        str_model = self.model.get_real_instance(self.get_object()).type
        str_model = f"{str_model}"
        print(str_model)
        return PAYMENT_UTILITY_FORMS[str_model][1]

    def test_func(self):
        payment = Payment.objects.get(pk=self.kwargs['pk'])
        if self.request.user.is_staff:
            return True
        return False

