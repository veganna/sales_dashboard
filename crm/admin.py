from django.contrib import admin
from .models import *
# Register your models here.

class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)

class NotesAdmin(admin.ModelAdmin):
    list_display = ('action', 'description', 'date')

class PropspectAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company', 'email', 'phone', 'linkedin', 'website', 'status', 'created_at', 'updated_at')

class TasksAdmin(admin.ModelAdmin):
    list_display = ('name', 'task', 'is_closed', 'end_date', 'created_at', 'updated_at')

class emailsAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', "recieved_time", "current_inbox")

admin.site.register(Status, StatusAdmin)
admin.site.register(Notes, NotesAdmin)
admin.site.register(Prospect, PropspectAdmin)
admin.site.register(Tasks, TasksAdmin)
admin.site.register(emailInbox, emailsAdmin)
