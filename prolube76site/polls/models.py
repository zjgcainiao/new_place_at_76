from operator import truediv
from unittest.util import _MAX_LENGTH
from django.db import models
import datetime
from django.utils import timezone
# added on 2022-10-29 so the load_env
import os
# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.
from dotenv import load_dotenv
# documentation for py-mssql is https://pymssql.readthedocs.io/en/stable/pymssql_examples.html#basic-features-strict-db-api-compliance
# import pymssql

# from prolube76site.polls.views import all_repair_orders 

class Question(models.Model):

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
       ## return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
        
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text



class RepairOrderReport(models.Model):
    repair_id=models.IntegerField()
    customer_name=models.CharField(max_length=60)
    repair_status=models.CharField(max_length=12)
    vin=models.IntegerField()
    vehicle_year=models.IntegerField()
    make=models.CharField(max_length=30)
    time_out=models.DateTimeField()
    last_visit_date=models.DateTimeField()
    repair_total_amt=models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self): 
        return self.repair_id 

    

