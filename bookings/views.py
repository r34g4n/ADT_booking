from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import  messages

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
