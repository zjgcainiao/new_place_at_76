from tabnanny import verbose
from venv import create
from django import db
from django.db import models

class NhtsaServiceBulletin(models.Model):
    id = models.BigAutoField(primary_key=True)
    bul_no = models.CharField(max_length=16, blank=True, null=True, 
                              db_index=True,verbose_name="Bulletin Number")
    bul_rep = models.CharField(max_length=16, blank=True, null=True,verbose_name="Replacement Bulletin")
    nhtsa_item_number = models.IntegerField(help_text="search for id field in the nhtsa flat file",db_index=True)
    bul_date = models.CharField(max_length=8, blank=True, null=True)
    complaint_name = models.CharField(max_length=300, blank=True, null=True, verbose_name="Complaint Name")
    make_txt = models.CharField(max_length=25, blank=True, null=True, verbose_name="Affected Make")
    model_txt = models.CharField(max_length=256, blank=True, null=True,verbose_name="Affected Model")
    year_txt = models.CharField(max_length=4, blank=True, null=True,verbose_name="Affected Vehicle Year")
    date_added = models.CharField(max_length=8, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # unique_together = (('year_txt', 'make_txt', 'model_txt','nhtsa_item_number','date_added'),)
        db_table = 'nthsa_service_bulletins'
        ordering = ['year_txt',  'make_txt', 'model_txt','nhtsa_item_number',]
        indexes = [
            models.Index(fields=['year_txt',  'make_txt', 'model_txt','nhtsa_item_number',]),
        ]