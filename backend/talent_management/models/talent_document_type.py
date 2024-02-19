from .base import models, timezone



class TalentDocumentType(models.Model):
    id = models.BigAutoField(primary_key=True)
    document_type = models.CharField(max_length=50,null=True, blank=True)
    document_type_description = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        db_table = 'talent_document_type'
        ordering = ['-id']