from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('view/all', views.PaymentsListView.as_view(), name='view_payment_all'),
    path('new/choose', views.choose_payment_to_post, name='choose_payment_to_post'),
    path('new/<str:choice>', views.create_payment, name='create_payment'),
    path('update-payment-home/', views.payment_update_home, name='payment_update_home'),
    path('update-payment/<int:pk>/', views.PatientPaymentListView.as_view(), name='update_payment'),
    path('payment/edit/<int:pk>/', views.PaymentUpdateView.as_view(), name='payment-edit'),
]