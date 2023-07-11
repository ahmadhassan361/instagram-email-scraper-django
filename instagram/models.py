from django.db import models

# Create your models here.
class ProcessController(models.Model):
    username = models.CharField(max_length=200,null=True,blank=True)
    file = models.CharField(max_length=200,null=True,blank=True)
    scraped_email = models.IntegerField(default=0)
    isRuning = models.BooleanField(default=True)
    isComplete = models.BooleanField(default=False)
    isStop = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    complete_date = models.DateTimeField(null=True,blank=True)
    list_data = models.JSONField(default=list)
    total_acc = models.IntegerField(default=0)
