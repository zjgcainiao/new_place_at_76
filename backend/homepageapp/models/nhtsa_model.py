from .base import models
from .nhtsa_make import NhtsaMake
from internal_users.models import InternalUser

class NhtsaModel(models.Model):
    id = models.AutoField(primary_key=True)
    make = models.ForeignKey(NhtsaMake, on_delete=models.CASCADE,related_name='nhtsa_models')
    model_id = models.IntegerField()
    model_name = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(InternalUser, on_delete=models.SET_NULL, null=True, related_name='nhtsa_models_created_by')
    updated_by = models.ForeignKey(InternalUser, on_delete=models.SET_NULL, null=True, related_name='nhtsa_models_updated_by')
    


    class Meta:
        db_table = 'nhtsa_models'
        unique_together = ('make', 'model_name')

    def __str__(self):
        return self.model_name