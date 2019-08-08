from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, UpdateView

from django.urls import reverse_lazy
from .models import Session
from users.models import Patient
from .forms import NewSessionStep1Form, NewSessionStep2Form

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
        'heading': 'primary info'
    }

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        """filling info for form 1"""
        patient = Patient.objects.filter(pk=request.session.get('patient_pk')).first()
        print(request.session.items())
        form1 = NewSessionStep1Form(initial={
            'patient': patient
        })
        """disabling form1"""
        for key in form1.fields.keys():
            print("foo: ", key)
            form1.fields[key].disabled = True
        """end of disabling form1"""
        """End of form1 info"""

        self.context['form1'] = form1
        self.context['form2'] = form

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # messages.success(request, "Valid data entered")

            """debugging print"""
            print(form.cleaned_data.items())
            for key, value in form.cleaned_data.items():
                if key == 'start_date':
                    request.session[key] = str(value)
                elif key == 'service':
                    request.session['service_pk'] = value.pk
                elif key == 'doctor':
                    request.session['doctor_pk'] = value.pk
                else:
                    request.session[key] = value

            print(request.session.items())
            """end of debugging print"""

            return render(request, self.template_name, context=None)
        self.context['form2'] = form
        return render(request, self.template_name, self.context)


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
