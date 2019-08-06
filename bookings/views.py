from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, UpdateView

from django.urls import reverse_lazy
from .models import Session
from .forms import NewSessionForm, SessionModelForm

# Create your views here.


class CreateSessionView(LoginRequiredMixin, View):

    form_class = NewSessionForm
    template_name = "bookings/bookings_home.html"
    context = {
        'title': 'Book Patient'
    }

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self.context['form1'] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            messages.success(request, "Valid data entered")
            return render(request, self.template_name, context=None)
        self.context['form1'] = form
        return render(request, self.template_name, self.context)


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


def redirect_to_home(request):
    return HttpResponseRedirect (reverse_lazy('bookings:bookings-home'))

# almost obsolete ------------------------------------------------------------------------------------------------------
@login_required
def create_session(request):
    context = {
        'title': 'Book Patient'
    }
    if request.method == "POST":
        form = NewSessionForm(request.POST)
        context['form2'] = form
        if form.is_valid():
            messages.success(request, "valid data entered")
            return render(request, 'bookings/bookings_home.html', context=None)
    else:
        form = NewSessionForm()
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
