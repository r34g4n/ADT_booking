from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.home, name='bookings-home'),
    path('session/view/all', views.SessionListView.as_view(), name='view_session_all'),
    path('session/new/', views.create_session, name='new_session')
]