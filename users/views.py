from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PatientRegistrationForm
from .models import Patient
# Create your views here.
@login_required
def register_patient(request):
    form = PatientRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        messages.success(request, f"The patient '{first_name} {last_name}' has been successfully registered")
        return redirect('bookings-home')
    else:
        form = PatientRegistrationForm()
    return render(request, 'users/users_register_patient.html', {'form': form})