from email.policy import default
from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Notes(models.Model):
    choices = (
        ('Linkedin DM', 'Linkedin DM'),
        ('Email', 'Email'),
        ('Call', 'Call'),
        ('Meeting', 'Meeting'),
        ('Interact', 'Interact'),
        ('Other', 'Other'),
    )
    action= models.CharField(max_length=255, choices=choices, blank=True, null=True)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.action + ' ' + str(self.date)


class Prospect(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    linkedin = models.URLField(max_length=255, blank=True)
    website = models.URLField(max_length=255, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    notes = models.ManyToManyField(Notes, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_status(self):
        return self.status.name

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Tasks(models.Model):
    choices = (
        ('Linkedin DM', 'Linkedin DM'),
        ('Email', 'Email'),
        ('Call', 'Call'),
        ('Meeting', 'Meeting'),
        ('Interact', 'Interact'),
        ('Other', 'Other'),
        
    )

    name = models.CharField(max_length=255, blank=True, null=True)
    task = models.CharField(max_length=255, choices=choices, blank=True, null=True)
    prospect = models.ForeignKey(Prospect, on_delete=models.DO_NOTHING, blank=True, null=True)
    is_closed = models.BooleanField(default=False)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.name




class emailInbox(models.Model):
    current_inbox = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sender = models.CharField(max_length=255, blank=True, null=True)
    recieved_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.current_inbox + ' ' + self.subject