from django.db import models
from internal_users.models import InternalUser
# models.py

# this model stores all result from the external API call to NHTSA
class NhtsaDecodedVin(models.Model):
    id = models.BigAutoField(primary_key=True)
    vin = models.CharField(max_length=30, unique=True, verbose_name="VIN")
    url = models.URLField(max_length=1500, null=True, blank=True, verbose_name="API URL")
    count = models.PositiveIntegerField()
    message = models.CharField(max_length=1000,null=True, blank=True)
    search_criteria = models.CharField(max_length=255,null=True, blank=True)
    results = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(InternalUser, on_delete=models.SET_NULL, null=True, related_name='nhtsa_decode_vins_created_by')
    updated_by = models.ForeignKey(InternalUser, on_delete=models.SET_NULL, null=True, related_name='nhtsa_decode_vins_updated_by')

    def __str__(self):
        return f" {self.vin}-{self.message}"
    
    class Meta:
        db_table = 'nhtsa_decoded_vins'
        ordering = ["-id", 'vin']
        indexes = [
            models.Index(fields=['vin',]),
        ]
        verbose_name = "NHTSA Decoded VIN"
        verbose_name_plural = "NHTSA Decoded VINs"