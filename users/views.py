# Other imports
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
# end of other imports


# mixins and generic views class imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
# end of generic views and mixins imports


# form imports
from .forms import PatientRegistrationForm
# end of form imports

"""end of forms imports"""

from users.models import Patient
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
