from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('session/view/all', views.SessionListView.as_view(), name='view_session_all'),
    path('session/new/1', views.CreateSessionStep1View.as_view(), name='new_session1'),
    path('session/new/2', views.CreateSessionStep2View.as_view(), name='new_session2'),
    path('session/new/3', views.CreateSessionStep3View.as_view(), name='new_session3'),
    path('session/new/claim-payment',
         views.CreateSessionClaimConservativePaymentView.as_view(),
         name='new_session_claim_conservative_payment'),
    path('session/<int:pk>/', views.SessionDetailView.as_view(), name='session-detail'),
    path('session/edit/<int:pk>/', views.SessionUpdate.as_view(), name='session-edit'),
    path('', views.home, name='bookings-home')
]