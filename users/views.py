# Other imports
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# end of other imports


# mixins and generic views class imports
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic import (
    ListView,
    UpdateView
)
from bookings.forms import NewSessionStep1Form
# end of generic views and mixins imports

# dal auto-complete imports
from dal import autocomplete
# end of dal auto-complete

# models import
from .models import Patient
# end of model imports

# form imports
from .forms import PatientRegistrationForm

# end of form imports

"""end of forms imports"""

from users.models import Patient

PATIENT_UPDATE_URL_ROOT = "/users/update-patient/"


# Create your views here.
@login_required
def register_patient(request):
    context = {
        'title': 'New Patient'
    }
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        context['form'] = form
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            messages.success(request, f"The patient '{first_name} {last_name}' has been successfully registered")
            success = [f"The patient '{first_name} {last_name}' has been successfully registered", ]

            # pop-up (messages and context)

            msgs = {}
            error = []
            warning = []
            msgs['success'] = [msg for msg in success]
            msgs['danger'] = [msg for msg in error]
            msgs['warning'] = [msg for msg in warning]
            context['msgs'] = msgs
            context['title'] = 'Success! close pop-up'

            # end of pop-up (messages and context)

            return render(request, template_name='users/logs_base.html', context=context)
    else:
        form = PatientRegistrationForm()
        context['form'] = form
    return render(request, 'users/users_register_patient.html', context)


class PatientsListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'users/patients_listview.html'
    context_object_name = 'patients'
    paginate_by = 10
    ordering = ['-last_modified']


def search_patient_home(request):
    if request.method == 'GET':
        q = (request.GET.get('q', None))
        if q == '':
            return redirect('bookings:bookings-home')
        return redirect('users:search_patient', q)
    return redirect('bookings:bookings-home')


class SearchPatients(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'users/patients_listview.html'
    context_object_name = 'patients'
    paginate_by = 10
    ordering = ['-date_added']

    def get_queryset(self):
        q = self.kwargs.get('q')
        if q is not None:
            try:
                int(q)
                qs = Patient.objects.filter(
                    Q(first_name__icontains=q) | Q(middle_name__icontains=q) | Q(last_name__icontains=q) | Q(
                        phone_number__icontains=q) | Q(uhid=q)
                )
            except ValueError:
                qs = Patient.objects.filter(
                    Q(first_name__icontains=q) | Q(middle_name__icontains=q) | Q(last_name__icontains=q) | Q(
                        phone_number__icontains=q)
                )
        else:
            qs = None
        return qs

class PatientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Patient
    template_name = 'users/users_update_patient.html'
    form_class = PatientRegistrationForm

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


def patient_update_home(request):
    context = {
        'other_form': NewSessionStep1Form()
    }
    if request.method == 'POST':
        form = NewSessionStep1Form(request.POST)
        if form.is_valid():
            patient = form.cleaned_data['patient']
            return redirect('users:update_patient', patient.pk)
        context['other_form'] = form
    return render(request, 'bookings/bookings_home.html', context=context)


class PatientAutocompleteView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = []
        if not self.request.user.is_authenticated:
            return Patient.objects.none()
        if self.q:
            qs = Patient.objects.filter(
                Q(first_name__icontains=self.q)| Q(middle_name__icontains=self.q) | Q(last_name__icontains=self.q) | Q(phone_number__icontains=self.q)
            )
        return qs
