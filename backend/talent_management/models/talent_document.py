from .base import models, timezone
from .talent import TalentsModel
from .talent_document_type import TalentDocumentType

class TalentDocuments(models.Model):
    document_id = models.BigAutoField(primary_key=True)
    talent = models.ForeignKey(
        TalentsModel, on_delete=models.SET_NULL, null=True)
    talent_document = models.FileField(
        upload_to='2024_talent_documents/',
        null=True, blank=True)  
    talent_uploaded_photos = models.ImageField(upload_to='talent_photos/',
                                               null=True, blank=True)
    uploaded_date = models.DateTimeField(default=timezone.now)
    document_type = models.ForeignKey(TalentDocumentType, 
                                      on_delete=models.DO_NOTHING, null=True, blank=True,
                                      related_name='talent_document_type')
    document_is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    uploaded_by = models.ForeignKey("internal_users.InternalUser", on_delete=models.DO_NOTHING, 
                                    null=True, blank=True,
                                    related_name='talent_document_uploaded_by'
                                    )

    class Meta:

        db_table = 'talent_documents'
        ordering = ['-document_id']

