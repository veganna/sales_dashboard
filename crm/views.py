from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .models import *
from django.contrib import messages
import json
from .email_grabber import get_inbox

# Create your views here.
class crmOverview(View):
    def get(self, request):
        return render(request, 'crm/crm-dash.html', {
            'tasks': Tasks.objects.filter(is_closed=False),
        })

    def put(self, request):
        data = json.loads(request.body)
        try:
            if data['action'] == 'add_note':
                id = data['id']
                note = data['note']
                task = Tasks.objects.get(id=id)
                prospect = task.prospect

                note = Notes(
                    action=task.name,
                    description=note
                )
                note.save()

                prospect.notes.add(note)
                prospect.save()
                return JsonResponse({'success': True})

            elif data['action'] == 'complete':
                task_id = data['id']
                task = Tasks.objects.get(id=task_id)
                task.is_closed = True
                task.save()
                return JsonResponse({'success': True})

            elif data['action'] == 'mass_complete':
                task_ids = data['ids']
                for task_id in task_ids:
                    print(task_id)
                    task = Tasks.objects.get(id=task_id)
                    task.is_closed = True
                    task.save()
                return JsonResponse({'success': True})

            else:
                return JsonResponse({'success': False})
        except Exception as e:
            return JsonResponse({'success': False})

    

class prospectDetails(View):
    def get(self, request, pk):
        return render(request, 'crm/prospect-detail.html', {'prospect': get_object_or_404(Prospect, pk=pk)})
    
class prospects(View):
    def post(self, request):
        if request.method == 'POST':
            if request.POST.get('first_name') and request.POST.get('email') and request.POST.get('phone') and request.POST.get('company'):
                saverecord = Prospect()
                saverecord.email = request.POST.get('email')
                saverecord.first_name = request.POST.get('first_name')
                saverecord.last_name = request.POST.get('last_name')
                saverecord.phone = request.POST.get('phone')
                saverecord.email = request.POST.get('email')
                saverecord.linkedin = request.POST.get('linkedin')              
                saverecord.company = request.POST.get('company')
                saverecord.status = Status.objects.get(id=request.POST.get('status'))
                
                try:
                    saverecord.save()
                    messages.success(request, 'Prospect added successfully')
                except:
                    messages.error(request, 'Error adding prospect')

            return render(request, 'crm/prospects.html', {
                'prospects': Prospect.objects.all().order_by('-created_at'),
                'status': Status.objects.all(),
            })  

    def delete(self, request):
        body = request.body
        body = json.loads(body) 
        for id in body['ids']:
            try:
                Prospect.objects.get(id=id).delete()
                messages.success(request, 'Prospect deleted successfully')
            except:
                messages.error(request, f'Error deleting prospect {id}')

        return JsonResponse({'success': True})
            
    def get(self, request):
        return render(request, 'crm/prospects.html', {
            'prospects': Prospect.objects.all().order_by('-created_at'),
            'status': Status.objects.all(),
        })


class editProspect(View):
    def post(self, request, pk):
        if request.method == 'POST':
            saverecord = Prospect.objects.get(id=pk)
            saverecord.first_name = request.POST.get('first_name')
            saverecord.last_name = request.POST.get('last_name')
            saverecord.company = request.POST.get('company')
            saverecord.email = request.POST.get('email')
            saverecord.phone = request.POST.get('phone')
            saverecord.linkedin = request.POST.get('linkedin')              
            saverecord.website = request.POST.get('website')
            saverecord.status = Status.objects.get(id=request.POST.get('status'))
            
            try:
                saverecord.save()
                return JsonResponse({'success': True})
                    
            except:
                return JsonResponse({'success': False})
                

class emails(View):
    def grab_all_emails(self, request):
        print("here")
        all_emails = get_inbox()
        if all_emails == True:
            print('check the dataabase')
        print("here2")
       
            

        
    def get(self, request):
        return render(request, 'crm/emails.html', {})

            
class emailDetails(View):
    def get(self, request):
        return render(request, 'crm/email-details.html', {})
   


