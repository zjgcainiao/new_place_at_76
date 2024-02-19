from tabnanny import verbose
from venv import create
from django import db
from django.db import models
from qrcode import make

# for each vehicle produced, there are types.
# https://api.nhtsa.gov/SafetyRatings/modelyear/2013/make/toyota/model/avalon
class NhtsaVehicleId(models.Model):
    id = models.BigAutoField(primary_key=True)
    vehicle_id = models.CharField(max_length=100, unique=True, db_index=True)
    vehicle_description = models.CharField(max_length=1000, null=True, blank=True)
    make = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    model_year = models.CharField(max_length=4, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'nhtsa_vehicle_ids'
        ordering = ["-id", 'vehicle_id']
        indexes = [
            models.Index(fields=['model_year','make','model','vehicle_id']),
        ]

    def __str__(self):
        return f"vehicle-id-{self.vehicle_id}-{self.make}-{self.model}-{self.model_year}"