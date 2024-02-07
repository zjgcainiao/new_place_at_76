from .base import models, InternalUser

from .category import CategoryModel
from .vendor import Vendors

class PartDescription(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    category = models.ForeignKey(
        CategoryModel, on_delete=models.SET_NULL, null=True,blank=True)
    vendor = models.ForeignKey(
        Vendors, on_delete=models.SET_NULL, null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        InternalUser, on_delete=models.DO_NOTHING, 
        related_name='part_description_created_by',
        null=True, blank=True)
    updated_by = models.ForeignKey(
        InternalUser, on_delete=models.DO_NOTHING, 
        related_name='part_description_updated_by'
        ,null=True, blank=True)
    
  
    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.updated_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'part_description_new_03'
        ordering = ["-id"]

