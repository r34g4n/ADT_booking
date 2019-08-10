from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, UpdateView
from django.utils.dateparse import parse_date

from django.urls import reverse_lazy
from .models import Session, Service
from payments.models import Payment
from users.models import Patient, Doctor
from payments.searches import get_conservative_unclaimed_payments
from .forms import NewSessionStep1Form, NewSessionStep2Form, NewSessionStep3NewPaymentForm

# Create your views here.


def redirect_to_home(request):
    return redirect('bookings:bookings-home')


@login_required
def home(request):
    if request.user.is_staff:
        # messages.info(request, "We've noticed that you have admin rights")
        # messages.warning(request, "You won't be able to utilize all your rights in this page")
        messages.info(request, "Kindly, navigate to the Admin page to utilize all your rights")
    context = {
        'title': 'Home'
    }
    return render(request,'bookings/bookings_home.html', context)


class CreateSessionStep1View(LoginRequiredMixin, View):

    form_class = NewSessionStep1Form
    template_name = "bookings/bookings_home.html"
    context = {
        'title': 'Book Patient',
        'heading': 'search patient'
    }

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self.context['form1'] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # messages.success(request, "Valid data entered")

            request.session['patient_pk'] = form.cleaned_data['patient'].pk
            return redirect('bookings:new_session2')
        self.context['form1'] = form
        return render(request, self.template_name, self.context)


class CreateSessionStep2View(LoginRequiredMixin, View):

    form_class = NewSessionStep2Form
    template_name = "bookings/bookings_home.html"
    context = {
        'title': 'Book Patient',
    }

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        """filling non-editable info into form 1"""
        patient = Patient.objects.filter(pk=request.session.get('patient_pk')).first()
        print(request.session.items())
        form1 = NewSessionStep1Form(initial={
            'patient': patient
        })
        """disabling form1"""
        for key in form1.fields.keys():
            form1.fields[key].disabled = True
        """end of disabling form1"""
        """End of form1 info"""

        self.context['form1'] = form1
        self.context['form2'] = form

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print("uncleaned form: ", request.POST)
        print("form is valid: ", form.is_valid())
        if form.is_valid():

            for key, value in form.cleaned_data.items():
                if key == 'start_date':
                    request.session[key] = str(value)
                elif key == 'service':
                    request.session['service_pk'] = value.pk
                elif key == 'doctor':
                    request.session['doctor_pk'] = value.pk
                else:
                    request.session[key] = value

            print("Form: ", form.cleaned_data.items())
            print("session: ", request.session.items())
            if request.session.get('payment_choice', None) == '2':
                return redirect('bookings:new_session_claim_conservative_payment')
            return redirect('bookings:new_session3')
        self.context['form2'] = form
        return render(request, self.template_name, self.context)


class CreateSessionClaimConservativePaymentView(LoginRequiredMixin, View):
    template_name = 'bookings/conservative_unclaimed_payment_form.html'
    context = {
        'title': 'Payment Detail',
        'heading': 'claim payment'
    }

    def get(self, request, *args, **kwargs):
        patient_pk = request.session.get('patient_pk', None)
        patient = Patient.objects.filter(pk=patient_pk).first()
        payments = get_conservative_unclaimed_payments(patient_pk).order_by('-date')
        self.context['conservative_unclaimed_payments'] = payments
        self.context['patient'] = patient
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        payment = request.POST.get('payment_id', None)

        """debug prints"""
        print(request.POST.get('payment_id', None))
        print(payment)
        """end of debug prints"""

        if request.POST.get('payment_id', None) is None:
            return redirect('bookings:new_session_claim_conservative_payment')

        payment = Payment.objects.get(pk=int(payment))

        if payment.patient.id != request.session.get('patient_pk', None):
            return redirect('bookings:new_session_claim_conservative_payment')
        else:
            request.session['payment'] = payment.pk
            messages.success(request, "Payment has been SUCCESSfully set aside for claiming")
            messages.success(request, "Almost there")
        return redirect('bookings:new_session_claim_conservative_payment')


class CreateSessionStep3View(LoginRequiredMixin, View):
    form_class = NewSessionStep3NewPaymentForm
    template_name = "bookings/bookings_home.html"
    context = {
        'title': 'Book Patient',
    }

    def get(self, request, *args, **kwargs):
        form = NewSessionStep3NewPaymentForm
        patient = Patient.objects.filter(pk=request.session.get('patient_pk')).first()
        form1 = NewSessionStep1Form(initial={
            'patient': patient
        })
        """disabling form1"""
        for key in form1.fields.keys():
            form1.fields[key].disabled = True
        """end of disabling form1"""
        """End of form1 info"""
        form2 = NewSessionStep2Form(initial={
            'start_date': parse_date(request.session.get('start_date', None)),
            'service': Service.objects.get(pk=request.session.get('service_pk', None)),
            'doctor': request.session.get('doctor_pk', None),
            'diagnosis': request.session.get('diagnosis', None),
            'payment_choice': request.session.get('payment_choice', None)
        })

        for key in form2.fields.keys():
            form2.fields[key].disabled = True

        self.context['form1'] = form1
        self.context['form2'] = form2
        self.context['form3'] = self.form_class

        return render(request, self.template_name, self.context)

    def post(self):
        pass


# almost obsolete ------------------------------------------------------------------------------------------------------
@login_required
def create_session(request):
    context = {
        'title': 'Book Patient'
    }
    if request.method == "POST":
        form = NewSessionStep1Form(request.POST)
        context['form2'] = form
        if form.is_valid():
            messages.success(request, "valid data entered")
            return render(request, 'bookings/bookings_home.html', context=None)
    else:
        form = NewSessionStep1Form()
        context['form2'] = form
    return render(request, 'bookings/bookings_home.html', context)
# ----------------------------------------------------------------------------------------------------------------------


class SessionListView(LoginRequiredMixin, ListView):
    model = Session
    template_name = 'bookings/session_listview.html'
    context_object_name = 'sessions'
    paginate_by = 10
    ordering = ['-start_date']


class SessionDetailView(LoginRequiredMixin, DetailView):
    model = Session


class SessionUpdate(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Session
    fields = ['service', 'doctor', 'doctor_diagnosis', 'start_date', 'remarks', 'status']
    success_message = "Session was successfully updated!"

    def test_func(self):
        session = self.get_object()
        if not session.is_past:
            return True
        return False
