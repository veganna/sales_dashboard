from django.db import models

# Create your models here.


class pipelineActivity(models.Model):
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)


    choices = None
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


    def __str__(self):
        return self.name

class pipeline(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class CustomerModel(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    linkedin = models.CharField(max_length=255)
    pipeline = models.ForeignKey(pipeline, on_delete=models.CASCADE)
    


class extraFieldModel(models.Model):
    fieldName = models.CharField(max_length=100)
    fieldVal = models.CharField(max_length=500)
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)

