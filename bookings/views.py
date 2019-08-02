from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


from .models import Session
from .forms import NewSessionForm

# Create your views here.


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


def create_session(request):
    form = NewSessionForm()
    context = {
        'form': form
    }
    return render(request, 'bookings/bookings_new_session.html' ,context)


class SessionListView(LoginRequiredMixin, ListView):
    model = Session
    template_name = 'bookings/session_listview.html'
    context_object_name = 'sessions'
    paginate_by = 10