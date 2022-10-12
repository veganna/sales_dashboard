from django.shortcuts import render
from django.views.generic import View

# Create your views here.
class crmOverview(View):
    def get(self, request):
        return render(request, 'crm/crm-dash.html')

