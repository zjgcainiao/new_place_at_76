from django.db import models
from internal_users.models import InternalUser

# this model stores all result from the external API call to NHTSA and associate it with any Vin record, if available
class NhtsaApiCallHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    vin = models.CharField(max_length=30, verbose_name="VIN",null=True,blank=True) # should not be unique because each record is a call to the API. so the same vin can be called multiple times
    url = models.URLField(max_length=1500, null=True, blank=True, verbose_name="API URL")
    count = models.PositiveIntegerField()
    message = models.CharField(max_length=1000,null=True, blank=True)
    search_criteria = models.CharField(max_length=255,null=True, blank=True)
    results = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(InternalUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="nhtsa_api_calls_created_by")
    updated_by = models.ForeignKey(InternalUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="nhtsa_api_calls_updated_by")
    
    @property
    def get_results(self):
        if self.results:
            return self.results.get('Results',{})

    def __init__(self):
        return f'{self.url}'

    class Meta:
        db_table = 'nhtsa_api_call_history'
        ordering = ["-id", 'vin']
        indexes = [
            models.Index(fields=['vin', 'url', '-created_at',]),
        ]