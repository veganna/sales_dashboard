from django.urls import path
from .views import *

app_name = 'CRM'

urlpatterns = [
    path('', crmOverview.as_view(), name='crmOverview'),
]