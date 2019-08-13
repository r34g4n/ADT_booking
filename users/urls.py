from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('view-patients/', views.PatientsListView.as_view(), name='view_patients'),
    path('patient-autocomplete', views.PatientAutocompleteView.as_view(), name='patient_autocomplete'),
]