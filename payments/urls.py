from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('new/choose', views.choose_payment_to_post, name='choose_payment_to_post'),
    path('new/<str:choice>', views.create_payment, name='create_payment')
]