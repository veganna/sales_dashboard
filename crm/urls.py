from django.urls import path
from .views import *

app_name = 'CRM'

urlpatterns = [
    path('', crmOverview.as_view(), name='crmOverview'),
    path('prospects/', prospects.as_view(), name='prospects'),
    path('prospects/<int:pk>/', prospectDetails.as_view(), name='prospectDetail'),
    path('prospects/<int:pk>/edit/', editProspect.as_view(), name='prospectEdit'),  
    path('emails/', emails.as_view(), name='emails'),
    path('email-details/', emailDetails.as_view(), name='emailDetail'),
]