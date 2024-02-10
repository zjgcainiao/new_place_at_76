from .base import models, InternalUser

class LaborRateDescription(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    labor_rate = models.DecimalField(null=True, blank=True, default=0.00, max_digits=9, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='labor_rate_description_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(
        InternalUser, related_name='labor_rate_description_updated', on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(
        null=True, auto_now=True)
    
    class Meta:
        db_table = 'laborratedescription_new_03'
        ordering = ["-id"]
        verbose_name = 'laborratedescription'
        verbose_name_plural = 'laborratedescriptions'
