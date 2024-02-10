from .base import models, InternalUser


class TaxesModel(models.Model):
    tax_id = models.AutoField(primary_key=True)
    tax_description = models.CharField(max_length=30, null=True)
    tax_applied_gl_code = models.IntegerField()
    tax_item_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='tax_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='tax_modified', on_delete=models.SET_NULL, null=True, blank=True)
    tax_last_updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'taxes_new_03'
        ordering = ["-tax_id"]
        verbose_name = 'tax'
        verbose_name_plural = 'taxes'

