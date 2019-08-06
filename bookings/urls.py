from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('session/view/all', views.SessionListView.as_view(), name='view_session_all'),
    path('session/new/', views.CreateSessionView.as_view(), name='new_session'),
    path('session/<int:pk>/', views.SessionDetailView.as_view(), name='session-detail'),
    path('session/edit/<int:pk>/', views.SessionUpdate.as_view(), name='session-edit'),
    path('', views.home, name='bookings-home')
]