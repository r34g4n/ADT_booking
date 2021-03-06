from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('view-patients/', views.PatientsListView.as_view(), name='view_patients'),
    path('update-patient-home/', views.patient_update_home, name='patient_update_home'),
    path('update-patient/<int:pk>/', views.PatientUpdateView.as_view(), name='update_patient'),
    path('search-patient/home/', views.search_patient_home, name='search_patient_home'),
    path('search-patient/<str:q>/', views.SearchPatients.as_view(), name='search_patient'),
    path('patient-autocomplete', views.PatientAutocompleteView.as_view(), name='patient_autocomplete'),
    path('patient/<int:pk>', views.PatientDetailView.as_view(), name='patient-detail'),
    path('reports/home', views.reports_home, name='reports_home'),
    path('reports/bookings/list', views.booking_listing_report, name='booking_listing_report'),
    path('reports/patients/list', views.patient_listing_report, name='patient_listing_report'),
    path('reports/payments/list', views.payment_listing_report, name='payment_listing_report')
]