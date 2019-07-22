from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('patient/', views.register_patient, name='register_patient')
]